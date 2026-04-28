function TextInputBox({ text, setText }) {
  return (
    <div className="card">
      <h2>Or Paste Prescription Text</h2>
      <p className="muted">
        Example: Tab Augmentin 625mg BD for 5 days after food.
      </p>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste prescription text here..."
        rows={8}
      />
    </div>
  );
}

export default TextInputBox;
