function Navbar() {
  return (
    <nav className="w-full border-b border-gray-400 bg-[#F6F4EC]">
      <div className="max-w-7xl mx-auto flex justify-between items-center px-8 py-5">

        <h1 className="text-3xl font-bold">
          Neuro<span className="text-amber-700">Vision.</span>
        </h1>

        <div className="flex gap-8 text-gray-700">

          <a href="#">Home</a>

          <a href="#">Upload MRI</a>

          <a href="#">Results</a>

          <a href="#">About</a>

        </div>

      </div>
    </nav>
  )
}

export default Navbar