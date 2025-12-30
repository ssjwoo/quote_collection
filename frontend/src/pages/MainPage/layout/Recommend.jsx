import { useNavigate } from "react-router-dom";

export const Recommend = ({ mode, recomQuote }) => {

  const navigation = useNavigate();

  const onDetail = (quote) => {
    navigation('/quote/' + quote.id, {
      state: {
        mode: mode,
        quote: quote // Pass the full quote object ok
      }
    })
  }

  return (
    <>
      <div className="flex-col flex items-center mb-12">
        <div className="mt-10 mb-4 text-3xl">RECOMMEND</div>
        {Array.isArray(recomQuote) && recomQuote.length > 0 ? (
          recomQuote.map((quote) => (
            <div key={quote.id} className="cursor-pointer mt-5 w-11/12 bg-new-bg h-full pt-5 pb-5 text-center rounded-lg shadow-lg" onClick={() => onDetail(quote)}>
              <div>{quote.content}</div>
            </div>
          ))
        ) : (
          <div className="mt-5 w-11/12 h-32 flex justify-center items-center bg-gray-100 rounded-lg shadow-inner text-gray-400">
            Loading recommendations...
          </div>
        )}
      </div>
    </>
  );
}