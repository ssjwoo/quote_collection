import { useEffect, useState } from "react";
import { Search } from "../../components/Search";
import { useNavigate, useParams, useLocation } from "react-router-dom";
import axios from "../../api/axios";

export const SearchList = () => {
  const navigation = useNavigate();
  const { input } = useParams();
  const location = useLocation();
  const [result, setResult] = useState([]);

  const highlightKeyword = (text, keyword) => {
    if (!keyword || !text) return text;
    const parts = text.split(new RegExp(`(${keyword})`, "gi"));
    return (
      <>
        {parts.map((part, i) =>
          part.toLowerCase() === keyword.toLowerCase() ? (
            <span key={i} className="bg-yellow-200">
              {part}
            </span>
          ) : (
            part
          )
        )}
      </>
    );
  };

  useEffect(() => {
    const fetchSearchResults = async () => {
      try {
        const queryParams = new URLSearchParams(location.search);
        const source_type = queryParams.get("source_type");

        let apiUrl = `/api/search/?q=${input}`;
        if (source_type) {
          apiUrl += `&source_type=${source_type}`;
        }

        const response = await axios.get(apiUrl);
        const data = response.data;

        const sourcesMap = new Map();
        data.sources.forEach((source) => sourcesMap.set(source.id, source));

        const combinedResults = [];
        const processedSourceIds = new Set();

        data.quotes.forEach((quote) => {
          const source = sourcesMap.get(quote.source_id);
          combinedResults.push({
            type: "quote",
            id: quote.id,
            content: quote.content,
            sourceTitle: source ? source.title : "Unknown",
            creator: source ? source.creator : "Unknown",
            source_type: source ? source.source_type : "Unknown",
          });
          if (source) {
            processedSourceIds.add(source.id);
          }
        });

        data.sources.forEach((source) => {
          if (!processedSourceIds.has(source.id)) {
            combinedResults.push({
              type: "source",
              id: source.id,
              title: source.title,
              creator: source.creator,
              source_type: source.source_type,
            });
          }
        });

        setResult(combinedResults);
      } catch (error) {
        console.error("Failed to fetch search results:", error);
      }
    };

    if (input) {
      fetchSearchResults();
    }
  }, [input, location.search]);

  const onDetail = (id) => {
    navigation("/quote/" + id, {
      state: {
        mode: source_type_from_url,
      },
    });
  };
  const queryParams = new URLSearchParams(location.search);
  const source_type_from_url = queryParams.get("source_type");

  return (
    <>
      <div className="flex justify-center">
        <Search prevInput={input} source_type={source_type_from_url} />
      </div>
      <div className="text-main-green flex mt-10 justify-center">
        " {input} " results
      </div>
      <div className="flex flex-col justify-items-center mt-7">
        {result.map((r) => (
          <div
            key={r.id}
            className=" cursor-pointer mt-5 border-2 hover:bg-main-beige border-main-green h-full pt-5 pb-5 text-center rounded-lg shadow-lg"
            onClick={() => onDetail(r.id)}
          >
            {r.type === "quote" ? (
              <>
                <div className=" pl-3 pb-3 text-sm text-start">
                  {highlightKeyword(r.sourceTitle, input)} ({r.source_type})
                </div>
                <div className="text-lg">
                  {highlightKeyword(r.content, input)}
                </div>
                <div className="text-sm text-gray-600">
                  {highlightKeyword(r.creator, input)}
                </div>
              </>
            ) : (
              <>
                <div className=" pl-3 pb-3 text-sm text-start">
                  {highlightKeyword(r.title, input)} ({r.source_type})
                </div>
                <div className="text-lg">Source</div>
                <div className="text-sm text-gray-600">
                  {highlightKeyword(r.creator, input)}
                </div>
              </>
            )}
          </div>
        ))}
      </div>
    </>
  );
};
