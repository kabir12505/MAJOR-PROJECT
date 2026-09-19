
import { useRef, useState } from "react";

function UploadBox({ onFileSelect }) {
  const inputRef = useRef();
  const [image, setImage] = useState(null);

  function handleFile(file) {
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      alert("Please upload an image");
      return;
    }

    setImage(URL.createObjectURL(file));
    onFileSelect(file);
  }

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png,image/jpg"
        hidden
        onChange={(e) => handleFile(e.target.files[0])}
      />

      <div
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          handleFile(e.dataTransfer.files[0]);
        }}
        className="border-2 border-dashed border-gray-400 rounded h-72 flex justify-center items-center cursor-pointer hover:border-amber-700 transition overflow-hidden"
      >
        {image ? (
          <img
            src={image}
            alt="Uploaded MRI"
            className="object-contain w-full h-full rounded"
          />
        ) : (
          <div className="text-center">
            <div className="text-5xl">🧠</div>
            <h2 className="mt-5 font-semibold">
              Upload Brain MRI
            </h2>
            <p className="text-gray-500">
              Click or Drag Image
            </p>
          </div>
        )}
      </div>
    </>
  );
}

export default UploadBox;