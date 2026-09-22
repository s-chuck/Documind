import { useState } from "react";

function Signup({ onBackToHome, onSignIn }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSignup(event) {
    event.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://localhost:8000/auth/register",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            name,
            email,
            password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to create your account."
        );
      }

      setSuccess(
        "Your account has been created. You can sign in now."
      );

      setName("");
      setEmail("");
      setPassword("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      {/* =================================================
          TOP NAV
      ================================================= */}

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

      {/* =================================================
          AUTH CONTENT
      ================================================= */}

      <main className="auth-content">
        <div className="auth-layout auth-layout-signup">
          {/* Left side */}
          <section className="auth-intro">
            <span className="auth-eyebrow">
              START HERE
            </span>

            <h1>
              Give your documents
              <br />
              somewhere to go.
            </h1>

            <p>
              Create your library once. Then come back
              whenever you need to find, understand, or
              ask something about what you've stored.
            </p>

            <div className="signup-benefits">
              <div className="signup-benefit">
                <span>01</span>

                <div>
                  <strong>
                    Keep everything together
                  </strong>

                  <p>
                    Store your documents in one organized
                    library.
                  </p>
                </div>
              </div>

              <div className="signup-benefit">
                <span>02</span>

                <div>
                  <strong>
                    Ask questions naturally
                  </strong>

                  <p>
                    Find information without manually
                    searching through every page.
                  </p>
                </div>
              </div>

              <div className="signup-benefit">
                <span>03</span>

                <div>
                  <strong>
                    See your sources
                  </strong>

                  <p>
                    Understand where your answers came from.
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
                <h2>Create your account</h2>

                <p>
                  Your document library starts here.
                </p>
              </div>
            </div>

            {error && (
              <div className="auth-error">
                {error}
              </div>
            )}

            {success && (
              <div className="auth-success">
                {success}
              </div>
            )}

            <form
              className="auth-form"
              onSubmit={handleSignup}
            >
              <label>
                <span>Name</span>

                <input
                  type="text"
                  value={name}
                  onChange={(event) =>
                    setName(event.target.value)
                  }
                  placeholder="Your name"
                  autoComplete="name"
                  required
                />
              </label>

              <label>
                <span>Email</span>

                <input
                  type="email"
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
                <span>Password</span>

                <input
                  type="password"
                  value={password}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                  placeholder="Create a password"
                  autoComplete="new-password"
                  required
                />
              </label>

              <button
                className="auth-submit"
                type="submit"
                disabled={loading}
              >
                {loading
                  ? "Creating account..."
                  : "Create account"}

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
                Already have an account?
              </span>

              <button
                onClick={onSignIn}
              >
                Sign in
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

export default Signup;