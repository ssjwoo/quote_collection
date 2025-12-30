import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../../../api/axios";

export const RecommendDetail = ({ mode, quote }) => {
  const navigation = useNavigate();
  const [quotes, setQuotes] = useState([]);

  const onDetail = (quote) => {
    navigation("/quote/" + quote.id, {
      state: {
        mode: mode,
        quote: quote,
      },
    });
  };

  useEffect(() => {
    const fetchRecommendations = async () => {
      if (!quote || !quote.content) return;

      try {
        const response = await axios.post(`/recommendations/related?limit=3`, {
          current_quote_content: quote.content,
        });
        console.log("Chain Recommendation Result:", response.data);
        setQuotes(response.data);
      } catch (error) {
        console.error("Failed to fetch chain recommendations:", error);
        // Fallback to mode-based if chain fails (optional)
      }
    };

    fetchRecommendations();
  }, [quote]); // Re-run when quote changes (infinite chain)
  return (
    <>
      <div className="flex-col flex items-center mb-12">
        <div className="mt-16 mb-4 text-3xl">Recommended Quotes</div>
        {quotes.map((quote) => (
          <div
            key={quote.id}
            className="mt-5 cursor-pointer w-11/12 border-2 border-main-green h-full pt-5 pb-5 text-center rounded-lg shadow-lg hover:bg-mypage-menu"
            onClick={() => onDetail(quote)}
          >
            <div>{quote.content}</div>
          </div>
        ))}
      </div>
    </>
  );
};
