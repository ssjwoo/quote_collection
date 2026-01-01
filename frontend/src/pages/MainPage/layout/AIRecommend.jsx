import React from "react";
import { useAIRecommendation } from "../../../hooks/useAIRecommendation";
import { BookCard } from "../../../components/Common/BookCard";

export const AIRecommend = () => {
    const { recommendations, loading, error, fetchRecommendations } = useAIRecommendation();

    return (
        <div className="flex flex-col items-center mb-12 px-4 md:px-0">
            <h2 className="mt-10 mb-6 text-2xl md:text-3xl font-bold text-gray-800 tracking-tight">
                AI BOOK PICK
            </h2>

            <div className="w-full max-w-4xl">
                {!recommendations.length && !loading && (
                    <div className="flex justify-center">
                        <button
                            onClick={() => fetchRecommendations()}
                            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-full shadow-lg transform active:scale-95 transition-all duration-200"
                        >
                            AI에게 책 추천받기
                        </button>
                    </div>
                )}

                {loading && (
                    <div className="mt-10 flex flex-col items-center">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
                        <p className="text-gray-500 font-medium">AI가 당신의 취향을 분석하고 있습니다...</p>
                    </div>
                )}

                {error && (
                    <div className="mt-5 p-4 bg-red-50 text-red-600 rounded-lg text-center border border-red-100">
                        {error}
                    </div>
                )}

                {!!recommendations.length && !loading && (
                    <div className="space-y-6">
                        {recommendations.map((book, index) => (
                            <BookCard key={index} book={book} />
                        ))}

                        <div className="mt-8 flex justify-center">
                            <button
                                onClick={() => fetchRecommendations(true)}
                                className="text-sm font-semibold text-blue-600 hover:text-blue-800 bg-blue-50 hover:bg-blue-100 px-6 py-2 rounded-full transition-colors duration-200 border border-blue-100"
                            >
                                AI에게 다른 책 추천받기
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};
