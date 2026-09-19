
import { useState } from "react";
import UploadBox from "./UploadBox";

const featureExtractors = [
  "ResNet50",
  "DenseNet121",
  "EfficientNet-B0",
];

const featureSelectors = [
  "Mutual Information",
  "RFE",
  "L1-based Selection",
];

const classifiers = [
  "SVM",
  "Random Forest",
  "MLP",
];

function OptionGroup({ title, options, selected, onSelect }) {
  return (
    <div className="mb-6">
      <h4 className="font-semibold mb-3">{title}</h4>

      <div className="grid grid-cols-3 gap-2">
        {options.map((option) => (
          <button
            key={option}
            type="button"
            onClick={() => onSelect(option)}
            className={`border rounded p-3 text-sm transition ${
              selected === option
                ? "bg-teal-800 text-white border-teal-800"
                : "bg-white hover:bg-teal-50 border-gray-300"
            }`}
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  );
}

function InferenceConsole() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const [extractor, setExtractor] = useState("");
  const [selector, setSelector] = useState("");
  const [classifier, setClassifier] = useState("");

  const selectedCombination =
    extractor && selector && classifier
      ? `${extractor} + ${selector} + ${classifier}`
      : "Choose all three options";

  async function handleAnalyze() {
    if (!selectedFile) {
      setError("Please upload an MRI image first.");
      return;
    }

    if (!extractor || !selector || !classifier) {
      setError("Please select all three model options.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("image", selectedFile);

    // Send selected pipeline options to the backend.
    formData.append("extractor", extractor);
    formData.append("selector", selector);
    formData.append("classifier", classifier);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/predict/",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error || data.detail || "Prediction failed."
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message || "Could not connect to the backend."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-6xl mx-auto mt-16 bg-[#F6F4EC] border border-gray-400 rounded">

      {/* Header */}
      <div className="flex justify-between items-center border-b border-gray-400 px-6 py-4">
        <h2 className="font-semibold tracking-widest uppercase">
          Inference Console
        </h2>

        <span className="text-sm text-gray-500">
          {loading ? "Processing..." : "API"}
        </span>
      </div>

      <div className="grid md:grid-cols-2">

        {/* Upload Section */}
        <div className="border-r border-gray-400 p-8">
          <h3 className="uppercase text-sm tracking-widest text-teal-700 mb-5">
            Upload Brain MRI
          </h3>

          <UploadBox
            onFileSelect={(file) => {
              setSelectedFile(file);
              setResult(null);
              setError("");
            }}
          />

          <h2 className="mt-5 font-semibold">
            Drop MRI Image Here
          </h2>

          <p className="text-gray-500 mt-2">
            JPG, PNG, JPEG
          </p>
        </div>

        {/* Model Selection */}
        <div className="p-8">
          <h3 className="uppercase text-sm tracking-widest text-teal-700 mb-5">
            Configure Model
          </h3>

          <OptionGroup
            title="1. Feature Extractor"
            options={featureExtractors}
            selected={extractor}
            onSelect={(value) => {
              setExtractor(value);
              setResult(null);
              setError("");
            }}
          />

          <OptionGroup
            title="2. Feature Selection"
            options={featureSelectors}
            selected={selector}
            onSelect={(value) => {
              setSelector(value);
              setResult(null);
              setError("");
            }}
          />

          <OptionGroup
            title="3. Classifier"
            options={classifiers}
            selected={classifier}
            onSelect={(value) => {
              setClassifier(value);
              setResult(null);
              setError("");
            }}
          />

          <div className="border border-teal-700 bg-amber-50 p-4 rounded">
            <p className="text-xs uppercase tracking-wider text-gray-500">
              Selected Combination
            </p>

            <p className="font-semibold mt-2">
              {selectedCombination}
            </p>

            <p className="text-xs text-gray-600 mt-2">
              3 × 3 × 3 = 27 possible combinations
            </p>
          </div>

          {result && (
            <div className="mt-6 border border-gray-400 rounded p-4">
              <h3 className="font-semibold">
                Prediction Result
              </h3>

              <p className="mt-3 text-lg font-bold text-teal-800">
                {result.prediction}
              </p>

              <p className="text-sm text-gray-600 mt-2">
                Model: {result.model}
              </p>

              <p className="text-xs text-gray-500 mt-3">
                {result.note}
              </p>
            </div>
          )}

          {error && (
            <p className="mt-5 text-red-700 text-sm">
              {error}
            </p>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="border-t border-gray-400 p-6">
        <button
          onClick={handleAnalyze}
          disabled={
            loading ||
            !selectedFile ||
            !extractor ||
            !selector ||
            !classifier
          }
          className="bg-black text-white px-8 py-3 rounded hover:bg-teal-800 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "Analyzing..." : "Analyze MRI Image"}
        </button>
      </div>

    </div>
  );
}

export default InferenceConsole;