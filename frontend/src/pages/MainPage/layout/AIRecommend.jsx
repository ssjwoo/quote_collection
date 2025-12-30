import { useState } from "react";
import { useAuth } from "../../../hooks/useAuth";
import { getAIRecommendations } from "../../../api/recommendation";

export const AIRecommend = () => {
    const { user, showAlert } = useAuth();
    const [recommendations, setRecommendations] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleGetRecommendations = async (refresh = false) => {
        if (!user) {
            showAlert("로그인이 필요한 서비스입니다.");
            return;
        }
        setLoading(true);
        setError(null);
        if (refresh) {
            setRecommendations(""); // Clear data to show loading state effectively
        }
        try {
            const response = await getAIRecommendations(refresh);
            setRecommendations(response.data);
        } catch (err) {
            setError("추천을 가져오는 중 오류가 발생했습니다.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex-col flex items-center mb-12">
            <div className="mt-10 mb-4 text-3xl">AI BOOK PICK</div>
            <div className="w-11/12 flex flex-col items-center">
                {!recommendations && !loading && (
                    <button
                        onClick={handleGetRecommendations}
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded shadow-lg transition duration-300"
                    >
                        내 취향 분석하여 책 추천받기
                    </button>
                )}

                {loading && (
                    <div className="mt-5 p-5 text-center animate-pulse text-gray-500">
                        AI가 당신의 취향을 분석하고 있습니다...
                    </div>
                )}

                {error && (
                    <div className="mt-5 text-red-500">
                        {error}
                    </div>
                )}

                {recommendations && (
                    <div className="mt-5 w-full max-w-4xl space-y-6">
                        {(() => {
                            let books = [];
                            if (Array.isArray(recommendations)) {
                                books = recommendations;
                            } else if (typeof recommendations === 'string') {
                                try {
                                    books = JSON.parse(recommendations);
                                } catch (e) {
                                    // If parsing fails, it might be a raw string message
                                    return (
                                        <div className="bg-white p-6 rounded-lg shadow-lg whitespace-pre-wrap leading-relaxed text-gray-800 border border-gray-200">
                                            {recommendations}
                                        </div>
                                    );
                                }
                            }

                            if (!Array.isArray(books)) {
                                return (
                                    <div className="bg-white p-6 rounded-lg shadow-lg whitespace-pre-wrap leading-relaxed text-gray-800 border border-gray-200">
                                        {String(recommendations)}
                                    </div>
                                );
                            }

                            return books.map((book, index) => (
                                <div key={index} className="flex bg-white p-6 rounded-lg shadow-lg border border-gray-200 hover:shadow-xl transition-shadow duration-300">
                                    <div className="flex-shrink-0 w-32 h-48 mr-6 bg-gray-100 rounded overflow-hidden relative">
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
                                    <div className="flex flex-col flex-grow justify-between">
                                        <div>
                                            <div className="flex justify-between items-start mb-2">
                                                <h3 className="text-xl font-bold text-gray-800">{book.title}</h3>
                                            </div>
                                            <p className="text-gray-600 text-sm mb-3 font-medium">{book.author}</p>
                                            <p className="text-gray-700 leading-relaxed text-sm mb-4 bg-gray-50 p-3 rounded">
                                                "{book.reason}"
                                            </p>
                                        </div>
                                        <div className="flex justify-end">
                                            {book.link && (
                                                <a
                                                    href={book.link}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    className="flex items-center text-white bg-green-500 hover:bg-green-600 px-4 py-2 rounded text-sm font-semibold transition-colors duration-200"
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
                            ));
                        })()}

                        <div className="mt-6 text-center">
                            <button
                                onClick={() => handleGetRecommendations(true)}
                                className="text-sm text-blue-500 hover:underline bg-white px-4 py-2 rounded shadow-sm border border-gray-200 hover:bg-gray-50"
                            >
                                다른 책 추천받기
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};
