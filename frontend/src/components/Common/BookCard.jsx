import React from 'react';

export const BookCard = ({ book }) => {
    return (
        <div className="flex flex-col md:flex-row bg-white p-4 md:p-6 rounded-lg shadow-lg border border-gray-200 hover:shadow-xl transition-shadow duration-300">
            {/* Image Section */}
            <div className="flex-shrink-0 w-full md:w-32 h-64 md:h-48 mb-4 md:mb-0 md:mr-6 bg-gray-100 rounded overflow-hidden relative">
                {book.image ? (
                    <img
                        src={book.image}
                        alt={book.title}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                            e.target.onerror = null;
                            e.target.style.display = 'none';
                            e.target.nextSibling.style.display = 'flex';
                        }}
                    />
                ) : null}
                <div className="w-full h-full flex items-center justify-center text-gray-400 text-sm bg-gray-200 absolute top-0 left-0" style={{ display: book.image ? 'none' : 'flex' }}>
                    <span>No Image</span>
                </div>
            </div>

            {/* Info Section */}
            <div className="flex flex-col flex-grow justify-between">
                <div>
                    <h3 className="text-lg md:text-xl font-bold text-gray-800 mb-1">{book.title}</h3>
                    <p className="text-gray-600 text-xs md:text-sm mb-3 font-medium">{book.author}</p>
                    <p className="text-gray-700 leading-relaxed text-sm mb-4 bg-gray-50 p-3 rounded italic">
                        "{book.reason}"
                    </p>
                </div>
                <div className="flex justify-end">
                    {book.link && (
                        <a
                            href={book.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="w-full md:w-auto flex justify-center items-center text-white bg-green-500 hover:bg-green-600 px-4 py-2 rounded text-sm font-semibold transition-colors duration-200"
                        >
                            알라딘에서 보기
                            <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                            </svg>
                        </a>
                    )}
                </div>
            </div>
        </div>
    );
};
