import React from "react";
import { AlertTriangle } from "lucide-react";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Visualization rendering error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex h-full w-full flex-col items-center justify-center rounded-lg bg-slate-900/50 p-4 text-center">
          <AlertTriangle className="mb-4 h-12 w-12 text-red-500" />
          <h3 className="mb-2 text-lg font-bold text-white">Rendering Error</h3>
          <p className="mb-4 text-sm text-slate-400">
            There was an issue displaying this part of the visualization.
          </p>
          <button
            onClick={() => this.setState({ hasError: false, error: null })}
            className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500"
          >
            Try to Recover
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
