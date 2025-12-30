import { useNavigate } from "react-router-dom";

export const Popular = ({ mode, popularQuote }) => {
  const navigation = useNavigate();
  // console.log(popularQuote);
  const onDetail = (id) => {
    // Construct a quote object that matches the QuoteRead schema expected by Detail page
    // because popularQuote has a flat structure (PopularQuoteResponse)
    const formattedQuote = {
      id: popularQuote.id,
      content: popularQuote.content,
      user_id: 0, // System
      source_id: 0,
      tags: popularQuote.tags || [],
      source: {
        title: popularQuote.title,
        creator: popularQuote.creator,
        source_type: mode
      }
    };

    navigation("/quote/" + id, {
      state: {
        mode: mode,
        quote: formattedQuote
      },
    });
  };

  return (
    <>
      <div className="flex-col flex items-center">
        <div className="mt-9 mb-4 text-3xl">POPULAR</div>
        {popularQuote && popularQuote.title ? (
          <div
            className=" cursor-pointer h-56 bg-sub-darkbeidge rounded-xl shadow-xl w-4/5 "
            onClick={() => onDetail(popularQuote.id)}
          >
            <div className=" h-1/6 flex justify-start p-3">
              {popularQuote.title}
            </div>
            <div className="h-4/6 flex justify-center p-3">
              {popularQuote.content}
            </div>
            <div className="h-1/6 flex justify-end pb-3 pr-3">
              {popularQuote.creator}
            </div>
          </div>
        ) : (
          <div className="h-56 flex justify-center items-center bg-sub-darkbeidge rounded-xl shadow-xl w-4/5 ">
            <p>Loading popular quote...</p>
          </div>
        )}
      </div>
    </>
  );
};
