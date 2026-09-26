import { useState } from "react";

function Login({ onBackToHome, onSignUp }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin(event) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://localhost:8000/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email,
            password: password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to sign in."
        );
      }

      localStorage.setItem(
        "access_token",
        data.access_token
      );

      window.location.href = "/";
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <header className="auth-navbar">
        <button
          className="auth-brand"
          onClick={onBackToHome}
        >
          <span className="auth-brand-mark">
            D
          </span>

          <span>DocuMind</span>
        </button>

        <button
          className="auth-back-button"
          onClick={onBackToHome}
        >
          ← Back to home
        </button>
      </header>

      <main className="auth-content">
        <div className="auth-layout">

          {/* Left side */}
          <section className="auth-intro">
            <span className="auth-eyebrow">
              WELCOME BACK
            </span>

            <h1>
              Your documents
              <br />
              are waiting.
            </h1>

            <p>
              Pick up where you left off. Your library,
              conversations, and document knowledge are
              right where you left them.
            </p>

            <div className="auth-document-preview">
              <div className="auth-preview-top">
                <span className="auth-preview-file">
                  PDF
                </span>

                <div>
                  <strong>
                    Project Handbook
                  </strong>

                  <span>
                    Your document library
                  </span>
                </div>

                <span className="auth-preview-check">
                  ✓
                </span>
              </div>

              <div className="auth-preview-lines">
                <span />
                <span />
                <span />
                <span />
              </div>

              <div className="auth-preview-question">
                <span>?</span>

                <div>
                  <small>
                    LAST CONVERSATION
                  </small>

                  <p>
                    What should I do first?
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Right side */}
          <section className="auth-card">
            <div className="auth-card-heading">
              <span className="auth-small-mark">
                D
              </span>

              <div>
                <h2>Sign in</h2>

                <p>
                  Continue to your DocuMind library.
                </p>
              </div>
            </div>

            {error && (
              <div className="auth-error">
                {error}
              </div>
            )}

            <form
              className="auth-form"
              onSubmit={handleLogin}
            >
              <label>
                <span>Email</span>

                <input
                  type="text/"
                  value={email}
                  onChange={(event) =>
                    setEmail(event.target.value)
                  }
                  placeholder="you@example.com"
                  autoComplete="email"
                  required
                />
              </label>

              <label>
                <div className="auth-label-row">
                  <span>Password</span>

                  <button
                    type="button"
                    className="auth-forgot"
                  >
                    Forgot password?
                  </button>
                </div>

                <input
                  type="password"
                  value={password}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  required
                />
              </label>

              <button
                className="auth-submit"
                type="submit"
                disabled={loading}
              >
                {loading
                  ? "Signing in..."
                  : "Sign in"}

                {!loading && <span>→</span>}
              </button>
            </form>

            <div className="auth-divider">
              <span />
              <small>OR</small>
              <span />
            </div>

            <div className="auth-switch">
              <span>
                Don't have a DocuMind account?
              </span>

              <button onClick={onSignUp}>
                Create one
              </button>
            </div>
          </section>
        </div>
      </main>

      <footer className="auth-footer">
        <span>
          DocuMind
        </span>

        <span>
          Your documents. Your answers.
        </span>
      </footer>
    </div>
  );
}

export default Login;