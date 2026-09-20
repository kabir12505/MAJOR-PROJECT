
import Navbar from "../Components/Navbar";
import InferenceConsole from "../Components/InferenceConsole";
import EvaluationDashboard from "../Components/EvaluationDashboard";

function Home() {
  return (
    <>
      <Navbar />

      <div className="max-w-7xl mx-auto px-8 py-20">
        <p className="uppercase tracking-[4px] text-teal-800 mb-5">
          Multi-Model Alzheimer's Detection
        </p>

        <h1 className="text-7xl font-bold leading-tight">
          Detect
          <span className="text-amber-700">
            {" "}Alzheimer's
          </span>
          <br />
          Using Deep Learning
        </h1>

        <p className="text-xl text-gray-600 mt-8 max-w-3xl">
          Upload a brain MRI image and explore predictions using
          27 machine learning pipelines combining three deep learning
          feature extractors—ResNet50, DenseNet121, and EfficientNet-B0—
          with three feature selection techniques and three classifiers.
        </p>
      </div>

      <InferenceConsole />

      <EvaluationDashboard />
    </>
  );
}

export default Home;
