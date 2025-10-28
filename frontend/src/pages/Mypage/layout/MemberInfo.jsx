import { useEffect, useState } from "react";
import { Form } from "react-router-dom";

export const MemberInfo = () => {
  // TODO: API call here
  /** dummy data */
  const [user, setUser] = useState({
    id: "username",
    pw: "prePassword",
    email: "user123@momentary.com",
  });

  const [name, setName] = useState(user.id);
  const [pw, setPw] = useState("");
  const [confirmedPw, setConfirmedPw] = useState("");
  const [error, setError] = useState({ nameE: "", pwE: "", confirmedPwE: "" });
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    if (user.id === name.trim()) setChecked(true);
    else setChecked(false);
  }, [name]);

  const onIdCheck = () => {
    // TODO: API call here
    /** db에 존재하는 username인지 중복체크한 데이터 조회 후 비교 */
    // setChecked(true);
  };

  const onsubmit = (e) => {
    e.preventDefault();

    /** 아무것도 변경되지 않은 경우 */
    if (user.id === name.trim() && !pw && !confirmedPw) {
      return;
    }

    if (!checked) {
      alert("아이디 중복확인이 필요합니다.");
      return;
    }
    if (!name.trim()) {
      alert("수정할 아이디를 입력해주세요");
      return;
    }

    if (pw === user.pw) {
      alert("이전과 동일한 비밀번호로는 변경이 불가합니다.");
      return;
    }

    const newError = { nameE: "", pwE: "", confirmedPwE: "" };
    /** 회원정보 수정 충족조건 */
    if (name.length < 3) {
      newError.nameE = "이름은 3자 이상으로 설정해주세요.";
    } else newError.nameE = "";

    if (pw || confirmedPw) {
      if (pw.length < 9) {
        newError.pwE = "비밀번호는 9자 이상으로 설정해주세요.";
      } else if (pw !== confirmedPw) {
        newError.confirmedPwE = "입력한 비밀번호와 동일하지 않습니다.";
      } else {
        newError.pw = "";
        newError.confirmedPwE = "";
      }
    }

    setError(newError);
    if (newError.nameE || newError.pwE || newError.confirmedPwE) return;
    else {
      setUser((prev) => ({ //setUser가 쓰이지 않아 여기서 사용했습니다
        ...prev,
        id: name.trim(),
        pw: pw ? pw : prev.pw, // 비밀번호 입력했을 때만 업데이트
      }));

      setChecked(false);
      setPw("");
      setConfirmedPw("");
      alert("회원정보 수정 완료");
    }
  };

  return (
    <>
      <Form className="flex flex-col mt-10">
        <div className="text-3xl mb-5">Member Info</div>
        <div className="flex items-end mt-3">
          <label className="w-1/5 text-end pb-2 pr-2">name</label>
          <input
            type="text"
            className="w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 shadow-gray-400 outline-main-green"
            placeholder="아이디를 입력하세요"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <div className="self-end ml-4">
            <button
              className=" p-0.5 pl-1 pr-1 text-xs border rounded-sm border-main-green hover:ring-1 hover:ring-main-green"
              onClick={onIdCheck}
            >
              중복 확인
            </button>
          </div>
        </div>
        {name.length < 3 && error.nameE && (
          <div className="text-xs w-4/6 mt-4 pl-3 flex justify-center text-red-700">
            {error.nameE}
          </div>
        )}
        <div className="flex items-end mt-3">
          <label className="w-1/5 text-end pb-2 pr-2">email</label>
          <input
            type="text"
            className="w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 bg-gray-300 text-gray-600 shadow-gray-400 outline-main-green"
            value={user.email}
            disabled
          />
        </div>
        <div className="flex items-end mt-3">
          <label className="w-1/5 text-end pr-2 pb-2">비밀번호</label>
          <input
            type="password"
            className="w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 shadow-gray-400 outline-main-green"
            placeholder="비밀번호를 입력하세요"
            value={pw}
            onChange={(e) => setPw(e.target.value)}
          />
        </div>
        {pw.length < 9 && error.pwE && (
          <div className="text-xs w-4/6 mt-4 pl-3 flex justify-center text-red-700">
            {error.pwE}
          </div>
        )}
        <div className="flex items-end mt-3">
          <label className="w-1/5 text-end pr-2 pb-2">비밀번호 확인</label>
          <input
            type="password"
            className="w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 shadow-gray-400 outline-main-green"
            placeholder="비밀번호를 다시 한번 입력해주세요"
            value={confirmedPw}
            onChange={(e) => setConfirmedPw(e.target.value)}
          />
        </div>
        {pw !== confirmedPw && error.confirmedPwE && (
          <div className="text-xs w-4/6 mt-4 pl-3 flex justify-center text-red-700">
            {error.confirmedPwE}
          </div>
        )}
        <div className="self-end">
          <button
            className="rounded-xl p-2 text-xs mr-20 mt-7 w-5/12 border border-main-green hover:bg-main-pink"
            onClick={onsubmit}
          >
            수정
          </button>
        </div>
      </Form>
    </>
  );
};
