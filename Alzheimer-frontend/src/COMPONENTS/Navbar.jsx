import logo from "../assets/college logo.jpg";

function Navbar() {
  return (
    <nav className="w-full border-b border-gray-400 bg-[#F6F4EC]">
      <div className="max-w-7xl mx-auto flex justify-between items-center px-8 py-5">

        <h1 className="flex items-center text-3xl font-bold gap-3">
          <img src={logo} alt="SSIPMT Raipur logo" className="h-15 w-auto rounded" />
          <span>
            SSIPMT<span className="text-amber-700">,Raipur</span>
          </span>
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