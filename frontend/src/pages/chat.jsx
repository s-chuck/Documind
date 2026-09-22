import { useEffect, useRef, useState } from "react";

function Chat() {
  const token = localStorage.getItem("access_token");

  const [documents, setDocuments] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [documentMenuOpen, setDocumentMenuOpen] = useState(false);

  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] =
    useState(null);

  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [avatarMenuOpen, setAvatarMenuOpen] = useState(false);

  const [openConversationMenu, setOpenConversationMenu] =
    useState(null);

  const [deletingConversation, setDeletingConversation] =
    useState(null);

  const [renamingConversation, setRenamingConversation] =
    useState(null);

  const [renameValue, setRenameValue] = useState("");

  const messagesEndRef = useRef(null);
  const composerRef = useRef(null);
  const renameInputRef = useRef(null);

  /* =====================================================
     DOCUMENTS
  ===================================================== */

  async function loadDocuments() {
    const response = await fetch(
      "http://localhost:8000/documents/?page=1&limit=100",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Failed to load documents"
      );
    }

    setDocuments(data.items);
  }

  /* =====================================================
     CONVERSATIONS
  ===================================================== */

  async function loadConversations() {
    const response = await fetch(
      "http://localhost:8000/conversations/",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Failed to load conversations"
      );
    }

    setConversations(data);

    if (data.length > 0 && !activeConversation) {
      await selectConversation(data[0]);
    }
  }

  async function selectConversation(conversation) {
    setActiveConversation(conversation);
    setOpenConversationMenu(null);
    setRenamingConversation(null);
    setError("");

    try {
      const response = await fetch(
        `http://localhost:8000/conversations/${conversation.id}/messages`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to load messages"
        );
      }

      setMessages(data);

      if (window.innerWidth <= 900) {
        setSidebarOpen(false);
      }
    } catch (err) {
      setError(err.message);
    }
  }

  async function createConversation() {
    setError("");

    try {
      const response = await fetch(
        "http://localhost:8000/conversations/",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: "New Conversation",
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to create conversation"
        );
      }

      setConversations((prev) => [data, ...prev]);
      setActiveConversation(data);
      setMessages([]);
      setOpenConversationMenu(null);
      setRenamingConversation(null);
      setError("");

      if (window.innerWidth <= 900) {
        setSidebarOpen(false);
      }
    } catch (err) {
      setError(err.message);
    }
  }

  /* =====================================================
     RENAME CONVERSATION
  ===================================================== */

  function startRenamingConversation(conversation) {
    setOpenConversationMenu(null);

    setRenamingConversation(conversation.id);
    setRenameValue(conversation.title);

    setTimeout(() => {
      renameInputRef.current?.focus();
      renameInputRef.current?.select();
    }, 0);
  }

  function cancelRenamingConversation() {
    setRenamingConversation(null);
    setRenameValue("");
  }

  async function saveRenamedConversation(conversationId) {
    const trimmedTitle = renameValue.trim();

    if (!trimmedTitle) {
      setError("Conversation title cannot be empty.");
      return;
    }

    const conversation = conversations.find(
      (item) => item.id === conversationId
    );

    if (!conversation) {
      cancelRenamingConversation();
      return;
    }

    if (trimmedTitle === conversation.title) {
      cancelRenamingConversation();
      return;
    }

    setError("");

    try {
      const response = await fetch(
        `http://localhost:8000/conversations/${conversationId}`,
        {
          method: "PATCH",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: trimmedTitle,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to rename conversation"
        );
      }

      setConversations((previous) =>
        previous.map((item) =>
          item.id === conversationId
            ? data
            : item
        )
      );

      if (activeConversation?.id === conversationId) {
        setActiveConversation(data);
      }

      cancelRenamingConversation();
    } catch (err) {
      setError(err.message);
    }
  }

  function handleRenameKeyDown(event, conversationId) {
    if (event.key === "Enter") {
      event.preventDefault();

      saveRenamedConversation(conversationId);
    }

    if (event.key === "Escape") {
      event.preventDefault();

      cancelRenamingConversation();
    }
  }

  /* =====================================================
     DELETE CONVERSATION
  ===================================================== */

  async function deleteConversation(conversationId) {
    const conversation = conversations.find(
      (item) => item.id === conversationId
    );

    if (!conversation) {
      return;
    }

    const confirmed = window.confirm(
      `Delete "${conversation.title}"?\n\nThis conversation will be permanently deleted.`
    );

    if (!confirmed) {
      setOpenConversationMenu(null);
      return;
    }

    setDeletingConversation(conversationId);
    setOpenConversationMenu(null);
    setError("");

    try {
      const response = await fetch(
        `http://localhost:8000/conversations/${conversationId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        let data = {};

        try {
          data = await response.json();
        } catch {
          // DELETE 204 responses have no JSON body.
        }

        throw new Error(
          data.detail || "Failed to delete conversation"
        );
      }

      const remainingConversations =
        conversations.filter(
          (item) => item.id !== conversationId
        );

      setConversations(remainingConversations);

      if (activeConversation?.id === conversationId) {
        setActiveConversation(null);
        setMessages([]);

        if (remainingConversations.length > 0) {
          await selectConversation(
            remainingConversations[0]
          );
        }
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setDeletingConversation(null);
    }
  }

  /* =====================================================
     CHAT
  ===================================================== */

  async function sendMessage(event) {
    event?.preventDefault();

    if (
      !question.trim() ||
      !activeConversation ||
      loading
    ) {
      return;
    }

    const currentQuestion = question.trim();

    setQuestion("");
    setLoading(true);
    setError("");

    setMessages((prev) => [
      ...prev,
      {
        id: `user-${Date.now()}`,
        role: "user",
        content: currentQuestion,
      },
    ]);

    try {
      const response = await fetch(
        "http://localhost:8000/chat/",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: currentQuestion,
            conversation_id: activeConversation.id,
            document_id: selectedDocument?.id || null,
            limit: 3,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to send message"
        );
      }

      setMessages((prev) => [
        ...prev,
        {
          id: `assistant-${Date.now()}`,
          role: "assistant",
          content: data.answer,
          sources: data.sources || [],
        },
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  /* =====================================================
     KEYBOARD
  ===================================================== */

  function handleComposerKeyDown(event) {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      sendMessage();
    }
  }

  /* =====================================================
     INITIAL LOAD
  ===================================================== */

  useEffect(() => {
    loadDocuments().catch((err) =>
      setError(err.message)
    );

    loadConversations().catch((err) =>
      setError(err.message)
    );
  }, []);

  /* =====================================================
     CLOSE CONVERSATION MENU WHEN CLICKING OUTSIDE
  ===================================================== */

  useEffect(() => {
    function handleDocumentClick(event) {
      if (
        !event.target.closest(
          ".conversation-row-menu-wrapper"
        )
      ) {
        setOpenConversationMenu(null);
      }
    }

    document.addEventListener(
      "click",
      handleDocumentClick
    );

    return () => {
      document.removeEventListener(
        "click",
        handleDocumentClick
      );
    };
  }, []);

  /* =====================================================
     AUTO FOCUS RENAME INPUT
  ===================================================== */

  useEffect(() => {
    if (renamingConversation !== null) {
      renameInputRef.current?.focus();
      renameInputRef.current?.select();
    }
  }, [renamingConversation]);

  /* =====================================================
     AUTO SCROLL
  ===================================================== */

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  /* =====================================================
     HELPERS
  ===================================================== */

  function getSelectedDocumentLabel() {
    return selectedDocument
      ? selectedDocument.name
      : "All documents";
  }

  function selectDocument(document) {
    setSelectedDocument(document);
    setDocumentMenuOpen(false);
  }

  function formatDistance(distance) {
    if (typeof distance !== "number") {
      return "—";
    }

    return distance.toFixed(3);
  }

  function logout() {
    localStorage.removeItem("access_token");
    window.location.reload();
  }

  /* =====================================================
     RENDER
  ===================================================== */

  return (
    <div
      className={`documind-chat-shell ${
        sidebarOpen
          ? "sidebar-visible"
          : "sidebar-hidden"
      }`}
    >
      {/* =================================================
          SIDEBAR
      ================================================= */}

      <aside className="chat-sidebar">
        <div className="chat-sidebar-top">
          <button
            className="sidebar-brand"
            onClick={() => {
              window.location.href = "/";
            }}
          >
            <span className="sidebar-brand-icon">D</span>
            <span>DocuMind</span>
          </button>

          <button
            className="sidebar-collapse"
            onClick={() => setSidebarOpen(false)}
            aria-label="Collapse sidebar"
          >
            <span>‹</span>
          </button>
        </div>

        <button
          className="new-chat-action"
          onClick={createConversation}
        >
          <span className="new-chat-plus">+</span>
          <span>New chat</span>

          <span className="new-chat-shortcut">
            Ctrl K
          </span>
        </button>

        <div className="conversation-area">
          <div className="conversation-heading">
            <span>Recent conversations</span>
          </div>

          <div className="conversation-list">
            {conversations.length === 0 ? (
              <div className="conversation-empty">
                No conversations yet.
              </div>
            ) : (
              conversations.map((conversation) => (
                <div
                  key={conversation.id}
                  className={`conversation-row ${
                    activeConversation?.id ===
                    conversation.id
                      ? "conversation-row-active"
                      : ""
                  }`}
                  onClick={() =>
                    renamingConversation !==
                      conversation.id &&
                    selectConversation(conversation)
                  }
                >
                  {renamingConversation ===
                  conversation.id ? (
                    <input
                      ref={renameInputRef}
                      className="conversation-rename-input"
                      value={renameValue}
                      onChange={(event) =>
                        setRenameValue(
                          event.target.value
                        )
                      }
                      onKeyDown={(event) =>
                        handleRenameKeyDown(
                          event,
                          conversation.id
                        )
                      }
                      onClick={(event) =>
                        event.stopPropagation()
                      }
                      onBlur={() =>
                        saveRenamedConversation(
                          conversation.id
                        )
                      }
                      maxLength={100}
                      aria-label="Rename conversation"
                    />
                  ) : (
                    <span className="conversation-row-title">
                      {conversation.title}
                    </span>
                  )}

                  {renamingConversation !==
                    conversation.id && (
                    <div
                      className="conversation-row-menu-wrapper"
                      onClick={(event) =>
                        event.stopPropagation()
                      }
                    >
                      <button
                        type="button"
                        className="conversation-row-menu-button"
                        onClick={() =>
                          setOpenConversationMenu(
                            (previous) =>
                              previous ===
                              conversation.id
                                ? null
                                : conversation.id
                          )
                        }
                        aria-label={`Options for ${conversation.title}`}
                      >
                        ···
                      </button>

                      {openConversationMenu ===
                        conversation.id && (
                        <div className="conversation-menu">
                          <button
                            type="button"
                            className="conversation-menu-item"
                            onClick={() =>
                              startRenamingConversation(
                                conversation
                              )
                            }
                          >
                            <span className="conversation-menu-icon">
                              ✎
                            </span>

                            <span>Rename</span>
                          </button>

                          <button
                            type="button"
                            className="conversation-menu-item conversation-delete-button"
                            onClick={() =>
                              deleteConversation(
                                conversation.id
                              )
                            }
                            disabled={
                              deletingConversation ===
                              conversation.id
                            }
                          >
                            <span className="conversation-menu-icon">
                              ×
                            </span>

                            <span>
                              {deletingConversation ===
                              conversation.id
                                ? "Deleting..."
                                : "Delete"}
                            </span>
                          </button>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        <div className="sidebar-footer">
          <div className="sidebar-footer-status">
            <span className="online-indicator" />

            <span>Workspace active</span>
          </div>
        </div>
      </aside>

      {/* =================================================
          MAIN
      ================================================= */}

      <main className="chat-main">
        {/* =================================================
            TOP NAV
        ================================================= */}

        <header className="chat-header">
          <div className="chat-header-left">
            {!sidebarOpen && (
              <button
                className="sidebar-expand"
                onClick={() => setSidebarOpen(true)}
                aria-label="Open sidebar"
              >
                ☰
              </button>
            )}

            <nav className="chat-tabs">
              <button className="chat-tab chat-tab-active">
                Chat
              </button>

              <button
                className="chat-tab"
                onClick={() => {
                  window.location.href = "/";
                }}
              >
                Library
              </button>
            </nav>
          </div>

          <div className="chat-header-right">
            <div className="avatar-wrapper">
              <button
                className="user-avatar"
                onClick={() =>
                  setAvatarMenuOpen(
                    (previous) => !previous
                  )
                }
                aria-label="Open account menu"
              >
                D
              </button>

              {avatarMenuOpen && (
                <div className="avatar-menu">
                  <div className="avatar-menu-user">
                    <strong>DocuMind User</strong>
                    <span>Workspace</span>
                  </div>

                  <div className="avatar-menu-divider" />

                  <button onClick={logout}>
                    Log out
                  </button>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* =================================================
            CONVERSATION HEADER
        ================================================= */}

        <div className="conversation-toolbar">
          <div className="conversation-toolbar-inner">
            <div>
              <h1>
                {activeConversation?.title ||
                  "New conversation"}
              </h1>
            </div>

            <div className="document-picker-wrapper">
              <button
                className={`document-picker ${
                  documentMenuOpen
                    ? "document-picker-open"
                    : ""
                }`}
                onClick={() =>
                  setDocumentMenuOpen(
                    (previous) => !previous
                  )
                }
              >
                <span className="document-picker-icon">
                  ▧
                </span>

                <span className="document-picker-label">
                  {getSelectedDocumentLabel()}
                </span>

                <span className="document-picker-chevron">
                  {documentMenuOpen ? "⌃" : "⌄"}
                </span>
              </button>

              {documentMenuOpen && (
                <div className="document-menu">
                  <button
                    className={`document-option ${
                      !selectedDocument
                        ? "document-option-active"
                        : ""
                    }`}
                    onClick={() =>
                      selectDocument(null)
                    }
                  >
                    <span className="document-option-icon">
                      ◫
                    </span>

                    <span>
                      <strong>
                        All documents
                      </strong>

                      <small>
                        Search your entire library
                      </small>
                    </span>

                    {!selectedDocument && (
                      <span className="document-check">
                        ✓
                      </span>
                    )}
                  </button>

                  {documents.map((document) => (
                    <button
                      key={document.id}
                      className={`document-option ${
                        selectedDocument?.id ===
                        document.id
                          ? "document-option-active"
                          : ""
                      }`}
                      onClick={() =>
                        selectDocument(document)
                      }
                    >
                      <span className="document-option-icon">
                        ▧
                      </span>

                      <span className="document-option-text">
                        <strong>
                          {document.name}
                        </strong>

                        <small>
                          {document.status}
                        </small>
                      </span>

                      {selectedDocument?.id ===
                        document.id && (
                        <span className="document-check">
                          ✓
                        </span>
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* =================================================
            ERROR
        ================================================= */}

        {error && (
          <div className="chat-error-banner">
            <span>{error}</span>

            <button
              onClick={() => setError("")}
            >
              ×
            </button>
          </div>
        )}

        {/* =================================================
            MESSAGES
        ================================================= */}

        <section className="chat-scroll-area">
          {!activeConversation ? (
            <div className="chat-empty">
              <div className="chat-empty-icon">
                D
              </div>

              <h2>
                Ask questions about your
                documents.
              </h2>

              <p>
                Create a conversation to start
                exploring your knowledge base.
              </p>

              <button
                className="empty-chat-button"
                onClick={createConversation}
              >
                Start a new chat
              </button>
            </div>
          ) : messages.length === 0 ? (
            <div className="chat-empty">
              <div className="chat-empty-icon">
                D
              </div>

              <h2>
                What would you like to know?
              </h2>

              <p>
                Ask DocuMind something about{" "}
                {getSelectedDocumentLabel()}.
              </p>
            </div>
          ) : (
            <div className="message-thread">
              {messages.map((message) => {
                const isUser =
                  message.role === "user";

                return (
                  <article
                    key={message.id}
                    className={`message-row ${
                      isUser
                        ? "message-row-user"
                        : "message-row-assistant"
                    }`}
                  >
                    {!isUser && (
                      <div className="assistant-avatar">
                        D
                      </div>
                    )}

                    <div
                      className={`message-content ${
                        isUser
                          ? "user-message-content"
                          : "assistant-message-content"
                      }`}
                    >
                      {!isUser && (
                        <div className="assistant-message-header">
                          <strong>DocuMind</strong>
                          <span>Assistant</span>
                        </div>
                      )}

                      <div
                        className={`message-bubble ${
                          isUser
                            ? "user-message-bubble"
                            : "assistant-message-bubble"
                        }`}
                      >
                        {message.content}
                      </div>

                      {!isUser &&
                        message.sources &&
                        message.sources.length >
                          0 && (
                          <div className="sources-container">
                            <div className="sources-title">
                              <span>
                                Sources
                              </span>

                              <span className="sources-count">
                                {
                                  message.sources
                                    .length
                                }
                              </span>
                            </div>

                            <div className="source-grid">
                              {message.sources.map(
                                (
                                  source,
                                  index
                                ) => (
                                  <div
                                    className="source-card"
                                    key={`${source.chunk_id}-${index}`}
                                  >
                                    <div className="source-card-top">
                                      <span className="source-index">
                                        {String(
                                          index + 1
                                        ).padStart(
                                          2,
                                          "0"
                                        )}
                                      </span>

                                      <span className="source-file-icon">
                                        ▧
                                      </span>

                                      <span className="source-name">
                                        {
                                          source.document_name
                                        }
                                      </span>
                                    </div>

                                    <div className="source-card-meta">
                                      <span>
                                        Chunk{" "}
                                        {
                                          source.chunk_index
                                        }
                                      </span>

                                      <span className="source-separator">
                                        ·
                                      </span>

                                      <span>
                                        Distance
                                      </span>

                                      <code>
                                        {formatDistance(
                                          source.distance
                                        )}
                                      </code>
                                    </div>
                                  </div>
                                )
                              )}
                            </div>
                          </div>
                        )}
                    </div>
                  </article>
                );
              })}

              {loading && (
                <article className="message-row message-row-assistant">
                  <div className="assistant-avatar">
                    D
                  </div>

                  <div className="message-content assistant-message-content">
                    <div className="assistant-message-header">
                      <strong>DocuMind</strong>
                      <span>Assistant</span>
                    </div>

                    <div className="assistant-message-bubble thinking-bubble">
                      <span className="thinking-dot" />
                      <span className="thinking-dot" />
                      <span className="thinking-dot" />

                      <span className="thinking-label">
                        Searching your documents...
                      </span>
                    </div>
                  </div>
                </article>
              )}

              <div ref={messagesEndRef} />
            </div>
          )}
        </section>

        {/* =================================================
            COMPOSER
        ================================================= */}

        <div className="composer-container">
          <form
            ref={composerRef}
            className="composer"
            onSubmit={sendMessage}
          >
            <textarea
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              onKeyDown={handleComposerKeyDown}
              placeholder="Ask DocuMind about your documents..."
              rows={1}
              disabled={loading}
            />

            <div className="composer-actions">
              <span className="keyboard-hint">
                <kbd>Enter</kbd>
                <span>to send</span>
              </span>

              <button
                type="submit"
                className="send-button"
                disabled={
                  loading ||
                  !question.trim() ||
                  !activeConversation
                }
                aria-label="Send message"
              >
                ↑
              </button>
            </div>
          </form>

          <div className="composer-disclaimer">
            DocuMind uses your selected documents
            to generate answers. Verify important
            information against the source.
          </div>
        </div>
      </main>
    </div>
  );
}

export default Chat;