import { Loader2 } from "lucide-react";

function LoadingSpinner() {
  return (
    <div className="loading">
      <Loader2 className="spin" size={32} />
      <p>Analyzing prescription...</p>
    </div>
  );
}

export default LoadingSpinner;
