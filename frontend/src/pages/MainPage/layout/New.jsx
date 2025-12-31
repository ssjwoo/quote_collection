import { useNavigate } from "react-router-dom";

export const New = ({ mode, newQuote }) => {

  const navigation = useNavigate();

  const onDetail = (id) => {
    navigation('/quote/' + id, {
      state: {
        mode: mode
      }
    })
  }

  return (
    <>
      <div className="flex-col flex items-center mb-12">
        <div className="mt-14 mb-4 text-3xl">{mode === "trends" ? "TODAY'S PICK" : "NEW"}</div>
        {Array.isArray(newQuote) && newQuote.map((quote) => (
          <div key={quote.id} className=" cursor-pointer mt-5 w-11/12 bg-new-bg h-full pt-5 pb-5 text-center rounded-lg shadow-lg" onClick={() => onDetail(quote.id)}>
            <div>{quote.content}</div>
          </div>
        ))}
      </div>
    </>
  );
}