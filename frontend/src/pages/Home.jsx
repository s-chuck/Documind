import { useState } from "react";

function Home({ onSignIn, onSignUp }) {
  const [activeFeature, setActiveFeature] = useState(0);

  const features = [
    {
      number: "01",
      title: "Keep your documents together",
      text: "Upload your notes, reports, guides, and PDFs into one place. Your library stays organized and available whenever you need it.",
    },
    {
      number: "02",
      title: "Ask instead of searching",
      text: "Ask questions in plain language and let DocuMind find the relevant parts of your documents.",
    },
    {
      number: "03",
      title: "See where the answer came from",
      text: "Answers are grounded in your documents, with sources that help you verify the information.",
    },
  ];

  return (
    <div className="home-page">

      {/* =========================
          NAVIGATION
      ========================== */}
      <header className="home-navbar">
        <button
          className="home-brand"
          onClick={() =>
            window.scrollTo({
              top: 0,
              behavior: "smooth",
            })
          }
        >
          <span className="home-brand-mark">D</span>
          <span className="home-brand-name">DocuMind</span>
        </button>

        <nav className="home-nav-links">
          <a
            href="#how-it-works"
            className="home-nav-link"
          >
            How it works
          </a>

          <a
            href="#why-documind"
            className="home-nav-link"
          >
            Why DocuMind
          </a>
        </nav>

        <div className="home-nav-actions">
          <button
            className="home-signin"
            onClick={onSignIn}
          >
            Sign in
          </button>

          <button
            className="home-get-started"
            onClick={onSignUp}
          >
            Get started
          </button>
        </div>
      </header>


      <main>

        {/* =========================
            HERO
        ========================== */}
        <section className="home-hero">

          <div className="home-hero-content">

            <div className="home-eyebrow">
              Your documents, understood
            </div>

            <h1>
              Stop searching.
              <span>Start asking.</span>
            </h1>

            <p className="home-hero-description">
              DocuMind gives you a simple way to understand
              the documents you already have. Upload them,
              ask questions, and get answers grounded in
              your own information.
            </p>

            <div className="home-hero-actions">

              <button
                className="home-primary-button"
                onClick={onSignUp}
              >
                Start with your documents
                <span>→</span>
              </button>

              <button
                className="home-secondary-button"
                onClick={onSignIn}
              >
                I already have an account
              </button>

            </div>

          </div>


          {/* Document visual */}
          <div className="home-visual">

            <div className="home-glow" />

            <div className="home-document">

              <div className="home-document-label">
                PROJECT HANDBOOK
              </div>

              <div className="home-document-title">
                Working with internal systems
              </div>

              <div className="home-document-line long" />
              <div className="home-document-line medium" />
              <div className="home-document-line short" />
              <div className="home-document-line long" />

              <div className="home-document-question">
                What is the process for requesting access
                to a new system?
              </div>

              <div className="home-document-line medium" />
              <div className="home-document-line short" />

              <div className="home-document-answer">

                <div className="home-document-answer-label">
                  DOCUMIND
                </div>

                <p>
                  Access requests should be submitted
                  through the internal service portal.
                </p>

              </div>

            </div>

          </div>

        </section>


        {/* =========================
            INTRO STRIP
        ========================== */}
        <section className="home-intro-strip">

          <div className="home-intro-inner">

            <p>
              Built for people who have{" "}
              <strong>
                information everywhere
              </strong>{" "}
              and answers nowhere.
            </p>

          </div>

        </section>


        {/* =========================
            HOW IT WORKS
        ========================== */}
        <section
          id="how-it-works"
          className="home-section"
        >

          <div className="home-section-inner">

            <div className="home-section-heading">

              <span>
                HOW IT WORKS
              </span>

              <h2>
                A quieter way to
                <br />
                work with information.
              </h2>

              <p>
                DocuMind is designed around a simple idea:
                your documents should be useful after you
                upload them, not just stored somewhere.
              </p>

            </div>


            <div className="home-features">

              {features.map((feature) => (
                <button
                  key={feature.number}
                  className="home-feature"
                  onClick={() =>
                    setActiveFeature(
                      Number(feature.number) - 1
                    )
                  }
                >

                  <span className="home-feature-number">
                    {feature.number}
                  </span>

                  <h3>
                    {feature.title}
                  </h3>

                  <p>
                    {feature.text}
                  </p>

                </button>
              ))}

            </div>

          </div>

        </section>


        {/* =========================
            WHY DOCUMIND
        ========================== */}
        <section
          id="why-documind"
          className="home-section home-why"
        >

          <div className="home-section-inner">

            <div className="home-section-heading">

              <span>
                WHY DOCUMIND
              </span>

              <h2>
                Your information
                <br />
                should remember itself.
              </h2>

              <p>
                Instead of opening five files, remembering
                where something was written, and searching
                through pages, you can ask a question directly.
              </p>

            </div>


            <div className="home-why-content">

              <div className="home-why-list">

                <div className="home-why-item">
                  <h3>
                    Everything in one place
                  </h3>

                  <p>
                    Keep your notes, reports, guides,
                    research, and other documents organized
                    inside one library.
                  </p>
                </div>


                <div className="home-why-item">
                  <h3>
                    Ask in plain language
                  </h3>

                  <p>
                    You don't need to remember filenames,
                    keywords, or where a particular piece
                    of information was written.
                  </p>
                </div>


                <div className="home-why-item">
                  <h3>
                    Answers you can verify
                  </h3>

                  <p>
                    DocuMind connects answers back to the
                    documents they came from.
                  </p>
                </div>

              </div>


              <div className="home-why-list">

                <div className="home-why-item">
                  <h3>
                    Built around your documents
                  </h3>

                  <p>
                    Your questions are answered using the
                    information inside the documents you
                    choose.
                  </p>
                </div>


                <div className="home-why-item">
                  <h3>
                    Keep building your library
                  </h3>

                  <p>
                    Add new documents whenever you need
                    them without losing the ones you've
                    already uploaded.
                  </p>
                </div>


                <div className="home-why-item">
                  <h3>
                    Less searching, more understanding
                  </h3>

                  <p>
                    The goal isn't another place to store
                    files. It's a simpler way to work with
                    the information inside them.
                  </p>
                </div>

              </div>

            </div>

          </div>

        </section>


        {/* =========================
            FINAL CTA
        ========================== */}
        <section className="home-cta">

          <h2>
            Give your documents
            <br />
            somewhere to go.
          </h2>

          <p>
            Start building your personal document library.
          </p>

          <button
            className="home-primary-button"
            onClick={onSignUp}
          >
            Get started
            <span>→</span>
          </button>

        </section>

      </main>


      {/* =========================
          FOOTER
      ========================== */}
      <footer className="home-footer">

        <span className="home-footer-brand">
          DocuMind
        </span>

        <span>
          Your documents. Your answers.
        </span>

      </footer>

    </div>
  );
}

export default Home;