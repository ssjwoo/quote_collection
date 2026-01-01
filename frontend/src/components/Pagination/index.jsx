import React from "react";

export const Pagination = ({ currentPage, totalPages, onPageChange }) => {
    if (totalPages <= 1) return null;

    const pages = [];
    for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
    }

    return (
        <div className="flex justify-center items-center space-x-2 mt-10 mb-6">
            <button
                onClick={() => onPageChange(currentPage - 1)}
                disabled={currentPage === 1}
                className="px-3 py-1 rounded-md border border-main-green text-main-green hover:bg-main-green hover:text-white disabled:opacity-30 disabled:hover:bg-transparent disabled:hover:text-main-green transition-colors"
            >
                이전
            </button>

            {pages.map((page) => (
                <button
                    key={page}
                    onClick={() => onPageChange(page)}
                    className={`w-8 h-8 rounded-md border flex items-center justify-center transition-all ${currentPage === page
                            ? "bg-main-green text-white border-main-green font-bold scale-110 shadow-md"
                            : "border-gray-300 text-gray-600 hover:border-main-green hover:text-main-green"
                        }`}
                >
                    {page}
                </button>
            ))}

            <button
                onClick={() => onPageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
                className="px-3 py-1 rounded-md border border-main-green text-main-green hover:bg-main-green hover:text-white disabled:opacity-30 disabled:hover:bg-transparent disabled:hover:text-main-green transition-colors"
            >
                다음
            </button>
        </div>
    );
};
