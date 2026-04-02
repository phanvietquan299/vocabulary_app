export default function FirstPage({ userId, onContinue, onReset, onNew }) {
    const hasUserId = Boolean(userId)

    function handleButton() {
        return <div className="d-flex flex-column flex-sm-row justify-content-center gap-3">
            <button
                type="button"
                className="btn btn-primary btn-lg px-4"
                disabled={!hasUserId}
                onClick={onContinue}
            >
                Continue
            </button>

            <button
                type="button"
                className="btn btn-outline-secondary btn-lg px-4"
                onClick={hasUserId ? onReset : onNew}
            >
                {hasUserId ? 'Reset' : 'New User'}
            </button>
        </div>
    }

    return (
        <main className="container-fluid min-vh-100 d-flex align-items-center justify-content-center bg-light">
            <section className="text-center">
                <h1 className="display-3 fw-bold mb-3">Vocabulary App</h1>
                <p className="text-secondary mb-4">
                    {hasUserId ? `Continue with your user ID: ${userId}` : 'User ID not found in the browser.'}
                </p>
                {handleButton()}

            </section>
        </main>
    )
}
