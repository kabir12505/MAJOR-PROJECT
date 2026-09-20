
import { useEffect, useMemo, useState } from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

const API_URL = "http://127.0.0.1:8000/api/evaluation/";

function EvaluationDashboard() {
  const [models, setModels] = useState([]);
  const [extractor, setExtractor] = useState("All");
  const [selector, setSelector] = useState("All");
  const [classifier, setClassifier] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchEvaluation() {
      try {
        const response = await fetch(API_URL);

        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();

        if (!Array.isArray(data)) {
          throw new Error("Unexpected API response format");
        }

        setModels(data);
      } catch (err) {
        setError(err.message || "Could not load evaluation data.");
      } finally {
        setLoading(false);
      }
    }

    fetchEvaluation();
  }, []);

  const filteredModels = useMemo(() => {
    return models.filter((model) => {
      return (
        (extractor === "All" || model.extractor === extractor) &&
        (selector === "All" || model.selector === selector) &&
        (classifier === "All" || model.classifier === classifier)
      );
    });
  }, [models, extractor, selector, classifier]);

  const averageTestAccuracy = useMemo(() => {
    const values = filteredModels
      .map((model) => Number(model.test_accuracy))
      .filter(Number.isFinite);

    if (!values.length) return null;

    return (
      (values.reduce((sum, value) => sum + value, 0) / values.length) *
      100
    );
  }, [filteredModels]);

  const averageValidationAccuracy = useMemo(() => {
    const values = filteredModels
      .map((model) => Number(model.validation_accuracy))
      .filter(Number.isFinite);

    if (!values.length) return null;

    return (
      (values.reduce((sum, value) => sum + value, 0) / values.length) *
      100
    );
  }, [filteredModels]);

  const chartData = filteredModels.map((model) => ({
    name: `${model.extractor} | ${model.selector} | ${model.classifier}`,
    testAccuracy: Number(model.test_accuracy) * 100,
    validationAccuracy: Number(model.validation_accuracy) * 100,
  }));

  const formatPercent = (value) =>
    Number.isFinite(value) ? `${value.toFixed(2)}%` : "N/A";

  const selectClass =
    "w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-sm outline-none focus:border-teal-700";

  return (
    <section className="mx-auto max-w-7xl px-6 py-16">
      <div className="mb-8">
        <p className="mb-3 text-sm font-semibold uppercase tracking-[3px] text-teal-800">
          Model Evaluation
        </p>

        <h2 className="text-4xl font-bold text-gray-900">
          Performance Dashboard
        </h2>

        <p className="mt-3 max-w-3xl text-gray-600">
          Compare validation and test accuracy across the trained
          feature extraction, feature selection, and classification
          pipelines.
        </p>
      </div>

      {loading && (
        <p className="rounded-xl bg-gray-100 p-5 text-gray-700">
          Loading evaluation results...
        </p>
      )}

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-5 text-red-700">
          <p className="font-semibold">Unable to load dashboard</p>
          <p className="mt-1 text-sm">{error}</p>
          <p className="mt-2 text-sm">
            Check that Django is running and the evaluation API is available.
          </p>
        </div>
      )}

      {!loading && !error && (
        <>
          {/* Summary cards */}
          <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
              <p className="text-sm text-gray-500">Models displayed</p>
              <p className="mt-2 text-3xl font-bold text-gray-900">
                {filteredModels.length}
              </p>
            </div>

            <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
              <p className="text-sm text-gray-500">
                Average test accuracy
              </p>
              <p className="mt-2 text-3xl font-bold text-teal-800">
                {averageTestAccuracy === null
                  ? "N/A"
                  : formatPercent(averageTestAccuracy)}
              </p>
            </div>

            <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
              <p className="text-sm text-gray-500">
                Average validation accuracy
              </p>
              <p className="mt-2 text-3xl font-bold text-amber-700">
                {averageValidationAccuracy === null
                  ? "N/A"
                  : formatPercent(averageValidationAccuracy)}
              </p>
            </div>
          </div>

          {/* Filters */}
          <div className="mb-8 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
            <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
              <h3 className="text-xl font-bold text-gray-900">
                Filter models
              </h3>

              <button
                type="button"
                onClick={() => {
                  setExtractor("All");
                  setSelector("All");
                  setClassifier("All");
                }}
                className="rounded-full border border-gray-300 px-4 py-2 text-sm font-medium hover:bg-gray-100"
              >
                Reset filters
              </button>
            </div>

            <div className="grid gap-4 md:grid-cols-3">
              <label className="space-y-2">
                <span className="text-sm font-medium text-gray-700">
                  Feature extractor
                </span>
                <select
                  className={selectClass}
                  value={extractor}
                  onChange={(e) => setExtractor(e.target.value)}
                >
                  <option value="All">All extractors</option>
                  <option value="ResNet50">ResNet50</option>
                  <option value="DenseNet121">DenseNet121</option>
                  <option value="EfficientNet-B0">EfficientNet-B0</option>
                </select>
              </label>

              <label className="space-y-2">
                <span className="text-sm font-medium text-gray-700">
                  Feature selector
                </span>
                <select
                  className={selectClass}
                  value={selector}
                  onChange={(e) => setSelector(e.target.value)}
                >
                  <option value="All">All selectors</option>
                  <option value="Mutual Information">
                    Mutual Information
                  </option>
                  <option value="RFE">RFE</option>
                  <option value="L1-based Selection">
                    L1-based Selection
                  </option>
                </select>
              </label>

              <label className="space-y-2">
                <span className="text-sm font-medium text-gray-700">
                  Classifier
                </span>
                <select
                  className={selectClass}
                  value={classifier}
                  onChange={(e) => setClassifier(e.target.value)}
                >
                  <option value="All">All classifiers</option>
                  <option value="SVM">SVM</option>
                  <option value="Random Forest">Random Forest</option>
                  <option value="MLP">MLP</option>
                </select>
              </label>
            </div>
          </div>

          {/* Accuracy chart */}
          <div className="mb-8 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
            <h3 className="mb-2 text-xl font-bold text-gray-900">
              Accuracy comparison
            </h3>

            <p className="mb-6 text-sm text-gray-500">
              Values are percentages. Use the filters above to narrow the
              comparison.
            </p>

            {chartData.length === 0 ? (
              <p className="py-10 text-center text-gray-500">
                No models match these filters.
              </p>
            ) : (
              <div className="h-[420px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={chartData}
                    margin={{ top: 10, right: 20, left: 5, bottom: 120 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="name"
                      angle={-35}
                      textAnchor="end"
                      interval={0}
                      height={140}
                      tick={{ fontSize: 10 }}
                    />
                    <YAxis
                      domain={[0, 100]}
                      tickFormatter={(value) => `${value}%`}
                    />
                    <Tooltip
                      formatter={(value) => `${Number(value).toFixed(2)}%`}
                    />
                    <Bar
                      dataKey="validationAccuracy"
                      name="Validation accuracy"
                      fill="#0f766e"
                    />
                    <Bar
                      dataKey="testAccuracy"
                      name="Test accuracy"
                      fill="#b45309"
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>

          {/* Results table */}
          <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
            <div className="border-b border-gray-200 p-6">
              <h3 className="text-xl font-bold text-gray-900">
                Detailed model results
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                Showing {filteredModels.length} of {models.length} records.
              </p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full min-w-[800px] text-left text-sm">
                <thead className="bg-gray-50 text-xs uppercase tracking-wide text-gray-600">
                  <tr>
                    <th className="px-5 py-4">Feature extractor</th>
                    <th className="px-5 py-4">Selector</th>
                    <th className="px-5 py-4">Classifier</th>
                    <th className="px-5 py-4">Validation</th>
                    <th className="px-5 py-4">Test</th>
                    <th className="px-5 py-4">Status</th>
                  </tr>
                </thead>

                <tbody className="divide-y divide-gray-100">
                  {filteredModels.map((model, index) => (
                    <tr
                      key={`${model.extractor}-${model.selector}-${model.classifier}-${index}`}
                      className="hover:bg-gray-50"
                    >
                      <td className="px-5 py-4 font-medium text-gray-900">
                        {model.extractor}
                      </td>
                      <td className="px-5 py-4">{model.selector}</td>
                      <td className="px-5 py-4">{model.classifier}</td>
                      <td className="px-5 py-4">
                        {formatPercent(
                          Number(model.validation_accuracy) * 100
                        )}
                      </td>
                      <td className="px-5 py-4 font-semibold text-teal-800">
                        {formatPercent(Number(model.test_accuracy) * 100)}
                      </td>
                      <td className="px-5 py-4">
                        <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-800">
                          {model.status || "Available"}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <p className="mt-5 text-sm leading-6 text-gray-500">
            Research prototype: accuracy metrics describe performance on
            the evaluation split and do not establish clinical diagnostic
            reliability.
          </p>
        </>
      )}
    </section>
  );
}

export default EvaluationDashboard;