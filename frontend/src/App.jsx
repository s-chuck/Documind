import { useState } from "react";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";

import Chat from "./pages/chat";
import Documents from "./pages/Documents";

function App() {
  const token = localStorage.getItem("access_token");

  /*
   * Authentication page shown before login.
   *
   * home  → landing page
   * login → sign in page
   * signup → registration page
   */
  const [authPage, setAuthPage] = useState("home");

  /*
   * Application page shown after login.
   *
   * documents → Library
   * chat      → Chat
   */
  const [page, setPage] = useState("documents");

  /* =====================================================
     AUTHENTICATED NAVIGATION
  ===================================================== */

  function goToLibrary() {
    setPage("documents");
  }

  function goToChat() {
    setPage("chat");
  }

  function logout() {
    localStorage.removeItem("access_token");

    setAuthPage("home");
    setPage("documents");

    window.location.reload();
  }

  /* =====================================================
     NOT LOGGED IN
  ===================================================== */

  if (!token) {
    if (authPage === "login") {
      return (
        <Login
          onBackToHome={() => setAuthPage("home")}
          onSignUp={() => setAuthPage("signup")}
        />
      );
    }

    if (authPage === "signup") {
      return (
        <Signup
          onBackToHome={() => setAuthPage("home")}
          onSignIn={() => setAuthPage("login")}
        />
      );
    }

    return (
      <Home
        onSignIn={() => setAuthPage("login")}
        onSignUp={() => setAuthPage("signup")}
      />
    );
  }

  /* =====================================================
     LOGGED IN
  ===================================================== */

  return (
    <div className="app">
      {/*
        Global navbar is intentionally shown only
        on the Library page.

        Chat has its own focused interface.
      */}

      {page === "documents" && (
        <nav className="navbar">
          <button
            className="brand"
            onClick={goToLibrary}
          >
            <span className="brand-mark">
              D
            </span>

            <span className="brand-name">
              DocuMind
            </span>
          </button>

          <div className="navbar-links">
            <button
              className="nav-active"
              onClick={goToLibrary}
            >
              Library
            </button>

            <button onClick={goToChat}>
              Chat
            </button>

            <button
              className="logout-button"
              onClick={logout}
            >
              Log out
            </button>
          </div>
        </nav>
      )}

      <main className="app-content">
        {page === "documents" && (
          <Documents
            onOpenChat={goToChat}
          />
        )}

        {page === "chat" && (
          <Chat
            onOpenLibrary={goToLibrary}
            onLogout={logout}
          />
        )}
      </main>
    </div>
  );
}

export default App;