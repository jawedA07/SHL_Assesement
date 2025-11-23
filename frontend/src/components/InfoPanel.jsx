import React from "react";

export default function InfoPanel() {
    return (
        <section className="w-full bg-white py-16 px-6 md:px-20 relative overflow-hidden">

            {/* Background Pattern Right Side */}
            <div className="absolute right-0 top-0 w-64 h-full opacity-20 pointer-events-none">
                <svg viewBox="0 0 200 400" fill="none" stroke="#0084c7" strokeWidth="4">
                    {Array.from({ length: 60 }).map((_, i) => (
                        <circle key={i} cx={Math.random() * 200} cy={Math.random() * 400} r="6" />
                    ))}
                </svg>
            </div>

            {/* Content */}
            <div className="max-w-5xl mx-auto relative z-10">

                {/* Dots Row */}
                <div className="flex gap-2 mb-6">
                    <div className="h-4 w-12 rounded-full bg-[#0084c7]"></div>
                    <div className="h-4 w-4 rounded-full bg-[#1f8bd2]"></div>
                    <div className="h-4 w-4 rounded-full bg-[#1f8bd2]"></div>
                    <div className="h-4 w-4 rounded-full bg-[#1f8bd2]"></div>
                </div>

                {/* Main Heading */}
                <h2 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight">
                    Find assessments that best meet your needs.
                </h2>

                {/* Description */}
                <p className="text-gray-700 text-lg mt-6 max-w-3xl leading-relaxed">
                    Browse through our extensive product catalog for science-backed
                    assessments that evaluate cognitive ability, personality, behavior,
                    skills, and more — by role and organizational level, by industry, and
                    by language.
                </p>

                

            </div>
        </section>
    );
}
