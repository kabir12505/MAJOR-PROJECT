import Navbar from "../components/Navbar";

function Home() {

  return (

    <>

      <Navbar />

      <div className="max-w-7xl mx-auto px-8 py-20">

        <p className="uppercase tracking-[4px] text-teal-800 mb-5">
          AI Powered Alzheimer's Detection
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

          Upload a brain MRI image and compare predictions from
          four state-of-the-art deep learning models including
          ResNet50, EfficientNetB0, DenseNet121 and Vision Transformer.

        </p>

      </div>

    </>

  );

}

export default Home;