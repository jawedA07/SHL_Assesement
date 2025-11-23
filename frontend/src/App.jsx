// import React from "react";
// import RecommendForm from "./components/RecommendForm";
// import Logo from "./assets/logo.png";

// export default function App() {
//   return (
//     <div className="min-h-screen w-full bg-gray-100">

//       {/* FULL-WIDTH HEADER */}
//       <header className="w-full bg-white/70 backdrop-blur-lg shadow-lg border-b border-gray-200 py-6 px-6 flex items-center justify-center relative">

//         {/* Logo on Left */}
//         <img
//           src={Logo}
//           alt="Logo"
//           className="absolute left-6 h-12 w-auto object-contain"
//         />

//         {/* Title + Subtitle Stack */}
//         <div className="text-center">
//           <h1 className="text-3xl font-semibold text-gray-900">
//             SHL Assessment Recommender
//           </h1>
//           <p className="text-gray-600 text-sm md:text-base mt-1">
//             Paste a job description or query to get personalized assessment recommendations.
//           </p>
//         </div>
//       </header>

//       {/* Main Content */}
//       <main className="w-full flex justify-center p-6 md:p-10">
//         <div className="w-full max-w-4xl">
//           <RecommendForm />
//         </div>
//       </main>

//     </div>
//   );
// }


import React from "react";
import RecommendForm from "./components/RecommendForm";
import InfoPanel from "./components/InfoPanel";
import Logo from "./assets/logo.png";

export default function App() {
  return (
    <div className="min-h-screen w-full bg-gray-100">

      {/* FULL WIDTH HEADER */}
      <header className="w-full bg-white/70 backdrop-blur-lg shadow-lg border-b border-gray-200 py-6 px-6 flex items-center justify-center relative">

        {/* Logo */}
        <img
          src={Logo}
          alt="Logo"
          className="absolute left-6 h-12 w-auto"
        />

        {/* Title + Subtitle Stack */}
        <div className="text-center">
          <h1 className="text-3xl font-semibold text-gray-900">
            SHL Assessment Recommender
          </h1>
          <p className="text-gray-600 text-sm md:text-base mt-1">
            Paste a job description or query to get personalized assessment recommendations.
          </p>
        </div>
      </header>

      {/* GAP ADDED HERE */}
      <div className="mt-10">
        <InfoPanel />
      </div>



      {/* Recommendation Form Section */}
      <main className="w-full px-6 md:px-16 py-10">
        <RecommendForm />
      </main>

    </div>
  );
}
