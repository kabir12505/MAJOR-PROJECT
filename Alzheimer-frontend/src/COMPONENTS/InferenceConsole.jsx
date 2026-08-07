import UploadBox from "./UploadBox";

function InferenceConsole() {
  return (
    <div className="max-w-6xl mx-auto mt-16 bg-[#F6F4EC] border border-gray-400 rounded">
      {/* Header */}
      <div className="flex justify-between items-center border-b border-gray-400 px-6 py-4">
        <h2 className="font-semibold tracking-widest uppercase">Inference Console</h2>
        <div className="flex gap-2">
          <div className="w-2 h-2 rounded-full bg-gray-400"></div>
          <div className="w-2 h-2 rounded-full bg-gray-400"></div>
          <div className="w-2 h-2 rounded-full bg-gray-400"></div>
        </div>
      </div>

      <div className="grid md:grid-cols-2">
        {/* Left Side */}
        <div className="border-r border-gray-400 p-8">
          <h3 className="uppercase text-sm tracking-widest text-teal-700 mb-5">Upload Brain MRI</h3>
          <UploadBox />
         
          <h2 className="mt-5 font-semibold">Drop MRI Image Here</h2>
          <p className="text-gray-500 mt-2">JPG, PNG, JPEG</p>
        </div>

        {/* Right Side */}
        <div className="p-8">
          <h3 className="uppercase text-sm tracking-widest text-teal-700 mb-5">Select Deep Learning Model</h3>
          <div className="space-y-4">
            <label className="flex justify-between border p-4 rounded cursor-pointer hover:bg-amber-50">
              <span>ResNet-18</span>
              <input type="radio" name="model" />
            </label>
            <label className="flex justify-between border p-4 rounded cursor-pointer hover:bg-amber-50">
              <span>EfficientNet-B0</span>
              <input type="radio" name="model" />
            </label>
            <label className="flex justify-between border p-4 rounded cursor-pointer hover:bg-amber-50">
              <span>ConvNeXt-Tiny</span>
              <input type="radio" name="model" />
            </label>
            <label className="flex justify-between border p-4 rounded cursor-pointer hover:bg-amber-50">
              <span>DenseNet-18</span>
              <input type="radio" name="model" />
            </label>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="border-t border-gray-400 p-6">
        <button className="bg-black text-white px-8 py-3 rounded hover:bg-teal-800">Analyze MRI Image</button>
      </div>
    </div>
  );
}

export default InferenceConsole;
