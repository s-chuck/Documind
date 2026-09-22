import { useEffect, useMemo, useState } from "react";

function Documents() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  async function loadDocuments() {
    try {
      const token = localStorage.getItem("access_token");

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
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleUpload(event) {
    const file = event.target.files[0];

    if (!file) return;

    setUploading(true);
    setError("");

    try {
      const token = localStorage.getItem("access_token");

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        "http://localhost:8000/documents/",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Upload failed"
        );
      }

      await loadDocuments();
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  }

  async function handleDelete(documentId) {
    const confirmed = window.confirm(
      "Delete this document? Its chunks will no longer be available for chat."
    );

    if (!confirmed) return;

    setError("");

    try {
      const token = localStorage.getItem("access_token");

      const response = await fetch(
        `http://localhost:8000/documents/${documentId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to delete document"
        );
      }

      setDocuments((prev) =>
        prev.filter(
          (document) => document.id !== documentId
        )
      );
    } catch (err) {
      setError(err.message);
    }
  }

  function getFileType(name) {
    const extension = name
      ?.split(".")
      .pop()
      ?.toLowerCase();

    if (extension === "pdf") return "PDF";
    if (extension === "docx") return "DOCX";
    if (extension === "txt") return "TXT";

    return "FILE";
  }

  const filteredDocuments = useMemo(() => {
    const query = search.trim().toLowerCase();

    if (!query) {
      return documents;
    }

    return documents.filter((document) =>
      document.name.toLowerCase().includes(query)
    );
  }, [documents, search]);

  const readyCount = documents.filter(
    (document) =>
      document.status?.toLowerCase() === "ready"
  ).length;

  useEffect(() => {
    loadDocuments();
  }, []);

  if (loading) {
    return (
      <div className="library-page loading-page">
        <div className="loading-line" />
        <p>Preparing your library...</p>
      </div>
    );
  }

  return (
    <div className="library-page">
      {/* =========================
          LIBRARY HEADER
      ========================= */}

      <section className="library-hero">
        <div>
          <p className="eyebrow">
            YOUR KNOWLEDGE BASE
          </p>

          <h1>Your Library</h1>

          <p className="library-intro">
            Everything you've given DocuMind to
            understand, in one place.
          </p>
        </div>

        <label className="library-upload-button">
          <span>
            {uploading
              ? "Processing..."
              : "+ Add document"}
          </span>

          <input
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={handleUpload}
            disabled={uploading}
            hidden
          />
        </label>
      </section>

      {/* =========================
          ERROR
      ========================= */}

      {error && (
        <div className="library-error">
          <div>
            <strong>Something went wrong</strong>
            <p>{error}</p>
          </div>

          <button
            onClick={() => setError("")}
          >
            ×
          </button>
        </div>
      )}

      {/* =========================
          LIBRARY TOOLBAR
      ========================= */}

      <section className="library-toolbar">
        <div className="library-stats">
          <span>
            {documents.length}{" "}
            {documents.length === 1
              ? "document"
              : "documents"}
          </span>

          <span className="toolbar-divider">
            /
          </span>

          <span className="ready-count">
            {readyCount} ready
          </span>
        </div>

        {documents.length > 0 && (
          <div className="library-search">
            <span>⌕</span>

            <input
              type="text"
              placeholder="Search your library..."
              value={search}
              onChange={(event) =>
                setSearch(event.target.value)
              }
            />

            {search && (
              <button
                onClick={() => setSearch("")}
                aria-label="Clear search"
              >
                ×
              </button>
            )}
          </div>
        )}
      </section>

      {/* =========================
          EMPTY LIBRARY
      ========================= */}

      {documents.length === 0 ? (
        <section className="library-empty">
          <div className="library-empty-art">
            <div className="paper paper-back" />
            <div className="paper paper-middle" />

            <div className="paper paper-front">
              <span />
              <span />
              <span />
            </div>
          </div>

          <p className="eyebrow">
            START HERE
          </p>

          <h2>
            Give DocuMind something
            <br />
            to work with.
          </h2>

          <p>
            Upload a document and you can ask
            questions about it, search through it,
            and explore what you've stored here.
          </p>

          <label className="primary-button">
            Add your first document

            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={handleUpload}
              hidden
            />
          </label>
        </section>
      ) : filteredDocuments.length === 0 ? (
        <section className="library-no-results">
          <div>⌕</div>

          <h2>No documents found</h2>

          <p>
            Nothing in your library matches
            "{search}".
          </p>

          <button
            className="secondary-button"
            onClick={() => setSearch("")}
          >
            Clear search
          </button>
        </section>
      ) : (
        /* =========================
           DOCUMENT LIST
        ========================= */

        <section className="library-list">
          <div className="library-list-header">
            <span>DOCUMENT</span>
            <span>STATUS</span>
            <span>ACTION</span>
          </div>

          {filteredDocuments.map((document) => {
            const status =
              document.status?.toLowerCase();

            return (
              <article
                className="library-document"
                key={document.id}
              >
                <div className="library-document-main">
                  <div
                    className={`file-badge file-${getFileType(
                      document.name
                    ).toLowerCase()}`}
                  >
                    {getFileType(document.name)}
                  </div>

                  <div className="library-document-info">
                    <h3>{document.name}</h3>

                    <p>
                      Document #{document.id}
                    </p>
                  </div>
                </div>

                <div className="library-document-status">
                  <span
                    className={`library-status ${status}`}
                  >
                    <span className="status-dot" />

                    {document.status}
                  </span>
                </div>

                <div className="library-document-actions">
                  <button
                    className="delete-document"
                    onClick={() =>
                      handleDelete(document.id)
                    }
                  >
                    Delete
                  </button>
                </div>
              </article>
            );
          })}
        </section>
      )}
    </div>
  );
}

export default Documents;