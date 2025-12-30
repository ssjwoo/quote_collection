import { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import { BookDetail } from "./layout/BookDetail";
import { MovieDetail } from "./layout/MovieDetail";
import { DramaDetail } from "./layout/DramaDetail";
import { RecommendDetail } from "./layout/RecommendDetail";
import axios from "../../api/axios";

export const Detail = () => {
  const { id } = useParams();
  const [quote, setQuote] = useState(null);

  const location = useLocation();

  useEffect(() => {
    // If quote is passed via state (e.g., from AI recommendations), use it directly
    if (location.state && location.state.quote) {
      setQuote(location.state.quote);
      return;
    }

    const fetchQuote = async () => {
      try {
        const response = await axios.get(`/quote/${id}`);
        setQuote(response.data);
      } catch (error) {
        console.error("Failed to fetch quote:", error);
      }
    };

    fetchQuote();
  }, [id, location.state]);

  if (!quote || !quote.source) {
    return <div>Loading...</div>;
  }

  const mode = quote.source.source_type;

  return (
    <>
      {mode === "book" && <BookDetail quote={quote} />}
      {mode === "movie" && <MovieDetail quote={quote} />}
      {mode === "drama" && <DramaDetail quote={quote} />}
      <RecommendDetail mode={mode} quote={quote} />
    </>
  );
};
