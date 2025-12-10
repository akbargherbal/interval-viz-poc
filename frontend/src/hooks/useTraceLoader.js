import { useState, useCallback, useEffect } from "react";

export const useTraceLoader = () => {
  const [trace, setTrace] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentAlgorithm, setCurrentAlgorithm] = useState("interval-coverage");
  const [availableAlgorithms, setAvailableAlgorithms] = useState([]);

  const BACKEND_URL =
    process.env.REACT_APP_API_URL || "http://localhost:5000/api";

  /**
   * Fetch list of available algorithms from registry.
   * This populates the algorithm selector dynamically.
   */
  const fetchAvailableAlgorithms = useCallback(async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/algorithms`);
      if (!response.ok) {
        console.warn("Failed to fetch algorithm list, using defaults");
        return;
      }
      const algorithms = await response.json();
      setAvailableAlgorithms(algorithms);
    } catch (err) {
      console.warn("Could not fetch algorithms:", err);
      // Non-critical error - app can still work with hardcoded algorithms
    }
  }, [BACKEND_URL]);

  /**
   * Format input data for specific algorithms when using unified endpoint.
   * Each algorithm may have different input format requirements.
   */
  const formatInputForUnifiedEndpoint = (algorithm, inputData) => {
    switch (algorithm) {
      case "interval-coverage":
        // IntervalCoverageTracer expects: {"intervals": [...]}
        return { intervals: inputData };
      
      case "binary-search":
        // BinarySearchTracer expects: {"array": [...], "target": ...}
        return inputData; // Already in correct format
      
      default:
        // Default: assume input is already correctly formatted
        return inputData;
    }
  };

  /**
   * Generic trace loader - supports multiple algorithms.
   *
   * Phase 2: Uses unified endpoint for registry-based algorithms,
   * falls back to legacy endpoints for backward compatibility.
   *
   * @param {string} algorithm - Algorithm identifier ('interval-coverage' or 'binary-search')
   * @param {object} inputData - Algorithm-specific input data
   */
  const loadTrace = useCallback(
    async (algorithm, inputData) => {
      setLoading(true);
      setError(null);
      setTrace(null); // Clear previous trace on new load attempt

      try {
        let endpoint;
        let requestBody;

        // Check if algorithm is in registry (uses unified endpoint)
        const isRegistryAlgorithm = availableAlgorithms.some(
          (alg) => alg.name === algorithm
        );

        if (isRegistryAlgorithm) {
          // Use unified endpoint for registry-based algorithms
          endpoint = `${BACKEND_URL}/trace/unified`;
          requestBody = {
            algorithm: algorithm,
            input: formatInputForUnifiedEndpoint(algorithm, inputData),
          };
        } else if (algorithm === "interval-coverage") {
          // FALLBACK: Legacy endpoint for Interval Coverage
          // Note: interval-coverage IS in registry, but this fallback handles
          // the race condition where availableAlgorithms hasn't loaded yet
          endpoint = `${BACKEND_URL}/trace`;
          requestBody = { intervals: inputData };
        } else {
          throw new Error(`Unknown algorithm: ${algorithm}`);
        }

        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          const errData = await response
            .json()
            .catch(() => ({ error: "Failed to parse error response" }));
          throw new Error(
            `Backend returned ${response.status}: ${
              errData.error || "Unknown error"
            }`
          );
        }

        const data = await response.json();
        setTrace(data);
        setCurrentAlgorithm(algorithm);
      } catch (err) {
        setError(
          `Backend error: ${err.message}. Please ensure the Flask backend is running on port 5000.`
        );
        console.error("Failed to load trace:", err);
      } finally {
        setLoading(false);
      }
    },
    [BACKEND_URL, availableAlgorithms]
  );

  /**
   * Load interval coverage trace (backward compatible).
   * Uses legacy endpoint as fallback during initial load.
   */
  const loadIntervalTrace = useCallback(
    (intervals) => {
      return loadTrace("interval-coverage", intervals);
    },
    [loadTrace]
  );

  /**
   * Load binary search trace.
   * Uses unified endpoint via registry.
   */
  const loadBinarySearchTrace = useCallback(
    (array, target) => {
      return loadTrace("binary-search", { array, target });
    },
    [loadTrace]
  );

  /**
   * Load example interval coverage trace (default on startup)
   */
  const loadExampleIntervalTrace = useCallback(() => {
    loadIntervalTrace([
      { id: 1, start: 540, end: 660, color: "blue" },
      { id: 2, start: 600, end: 720, color: "green" },
      { id: 3, start: 540, end: 720, color: "amber" },
      { id: 4, start: 900, end: 960, color: "purple" },
    ]);
  }, [loadIntervalTrace]);

  /**
   * Load example binary search trace
   */
  const loadExampleBinarySearchTrace = useCallback(() => {
    loadBinarySearchTrace([1, 3, 5, 7, 9, 11, 13, 15], 7);
  }, [loadBinarySearchTrace]);

  // Fetch available algorithms on mount
  useEffect(() => {
    fetchAvailableAlgorithms();
  }, [fetchAvailableAlgorithms]);

  // Initial load effect - loads interval coverage by default (backward compatible)
  useEffect(() => {
    loadExampleIntervalTrace();
  }, [loadExampleIntervalTrace]);

  return {
    trace,
    loading,
    error,
    currentAlgorithm,
    availableAlgorithms, // NEW: List of algorithms from registry
    // Generic loader
    loadTrace,
    // Algorithm-specific loaders
    loadIntervalTrace,
    loadBinarySearchTrace,
    // Example loaders
    loadExampleIntervalTrace,
    loadExampleBinarySearchTrace,
    // Utility
    fetchAvailableAlgorithms,
    setTrace,
  };
};