import { useEffect, useState } from "react";
import { Form } from "react-router-dom";
import axios from "../../../api/axios";

export const MemberInfo = () => {
  const [user, setUser] = useState(null);
  const [name, setName] = useState("");
  const [pw, setPw] = useState("");
  const [confirmedPw, setConfirmedPw] = useState("");
  const [error, setError] = useState({ nameE: "", pwE: "", confirmedPwE: "" });
  const [usernameStatus, setUsernameStatus] = useState("idle"); // 'idle', 'checking', 'available', 'unavailable', 'error'

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem("accessToken");
        if (token) {
          const response = await axios.get("/auth/me", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          const userData = response.data;
          setUser(userData);
          setName(userData.username);
          setUsernameStatus("available"); // Assume initial username is available
        } else {
          // Handle error
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
      }
    };
    fetchUser();
  }, []);

  useEffect(() => {
    if (user && user.username === name.trim()) {
      setUsernameStatus("available"); // Current username is always available
    } else if (usernameStatus !== "checking") {
      setUsernameStatus("idle"); // Reset status if username changes and not checking
    }
  }, [name, user]);

  const onIdCheck = async () => {
    if (!name.trim()) {
      setError((prev) => ({ ...prev, nameE: "아이디를 입력해주세요." }));
      setUsernameStatus("unavailable");
      return;
    }
    if (name.trim().length < 3) {
      setError((prev) => ({
        ...prev,
        nameE: "아이디는 3자 이상으로 설정해주세요.",
      }));
      setUsernameStatus("unavailable");
      return;
    }

    setUsernameStatus("checking");
    setError((prev) => ({ ...prev, nameE: "" }));
    try {
      const response = await axios.post("/users/check-name", {
        username: name,
      });
      const data = response.data;
      if (data.is_available) {
        setUsernameStatus("available");
      } else {
        setUsernameStatus("unavailable");
      }
    } catch (error) {
      console.error("Failed to check name:", error);
      setUsernameStatus("error");
    }
  };

  const onsubmit = async (e) => {
    e.preventDefault();

    if (user && user.username === name.trim() && !pw && !confirmedPw) {
      return;
    }

    if (usernameStatus === "unavailable") {
      alert("이미 사용중인 아이디입니다. 다시 확인해주세요.");
      return;
    }
    if (usernameStatus === "idle" && user.username !== name.trim()) {
      alert("아이디 중복확인이 필요합니다.");
      return;
    }
    if (!name.trim()) {
      alert("수정할 아이디를 입력해주세요");
      return;
    }

    const newError = { nameE: "", pwE: "", confirmedPwE: "" };
    if (name.length < 3) {
      newError.nameE = "이름은 3자 이상으로 설정해주세요.";
    }

    if (pw || confirmedPw) {
      if (pw.length < 9) {
        newError.pwE = "비밀번호는 9자 이상으로 설정해주세요.";
      } else if (pw !== confirmedPw) {
        newError.confirmedPwE = "입력한 비밀번호와 동일하지 않습니다.";
      }
    }

    setError(newError);
    if (newError.nameE || newError.pwE || newError.confirmedPwE) return;

    try {
      const token = localStorage.getItem("accessToken");
      const updatedUser = {
        username: name.trim(),
      };
      if (pw) {
        updatedUser.password = pw;
      }

      const response = await axios.put(`/users/${user.id}`, updatedUser, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      console.log(`/api/users/${user.id}`, response);

      const updatedUserData = response.data;
      setUser(updatedUserData);
      setName(updatedUserData.username);
      setPw("");
      setConfirmedPw("");
      alert("회원정보 수정 완료");
    } catch (error) {
      console.error("Failed to update user:", error);
    }
  };

  const getNameInputClass = () => {
    let baseClass =
      "w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 shadow-gray-400";
    if (usernameStatus === "available")
      return baseClass + " outline-main-green border border-main-green";
    if (usernameStatus === "unavailable")
      return baseClass + " outline-red-500 border border-red-500";
    return baseClass + " outline-main-green"; // Default or idle state
  };

  const getNameFeedbackMessage = () => {
    if (user && user.username === name.trim() && usernameStatus === "available")
      return "(현재 아이디)";
    if (usernameStatus === "checking") return "(중복 확인 중...)";
    if (usernameStatus === "available") return "(사용 가능한 아이디입니다.)";
    if (usernameStatus === "unavailable")
      return "(이미 사용중인 아이디입니다.)";
    if (usernameStatus === "error") return "(아이디 확인 중 오류 발생)";
    return "";
  };

  const getNameFeedbackColorClass = () => {
    if (usernameStatus === "available") return "text-main-green";
    if (usernameStatus === "unavailable") return "text-red-500";
    return "";
  };

  return (
    <>
      <Form className="flex flex-col mt-10">
        <div className="text-3xl mb-5">Member Info</div>
        <div className="flex items-end mt-3">
          <label className="w-1/5 text-end pb-2 pr-2">name</label>
          <input
            type="text"
            className={getNameInputClass()}
            placeholder="아이디를 입력하세요"
            value={name}
            onChange={(e) => {
              setName(e.target.value);
              setUsernameStatus((prev) =>
                user && user.username === e.target.value.trim()
                  ? "available"
                  : "idle"
              ); // Reset status on change unless it's current user's username
            }}
          />
          <div className="self-end ml-4">
            <button
              className="p-0.5 pl-1 pr-1 text-xs border rounded-sm border-main-green hover:ring-1 hover:ring-main-green
             disabled:border-gray-400 disabled:text-gray-400 disabled:hover:ring-0 "
              onClick={onIdCheck}
              disabled={
                usernameStatus === "checking" ||
                (user && user.username === name.trim())
              }
            >
              중복 확인
            </button>
          </div>
        </div>
        {(error.nameE || usernameStatus !== "idle") && (
          <div className="flex items-end mt-1">
            <div className="w-1/5"></div> {/* Spacer to match the label */}
            <div className={`text-xs ml-3 ${getNameFeedbackColorClass()}`}>
              {error.nameE || getNameFeedbackMessage()}
            </div>
          </div>
        )}

        {user && (
          <div className="flex items-end mt-3">
            <label className="w-1/5 text-end pb-2 pr-2">email</label>
            <input
              type="text"
              className="w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 bg-gray-300 text-gray-600 shadow-gray-400 outline-main-green"
              value={user.email}
              disabled
            />
          </div>
        )}
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
            className="rounded-xl p-2 text-xs mr-20 mt-7 w-5/12 border border-main-green hover:bg-mypage-menu"
            onClick={onsubmit}
          >
            수정
          </button>
        </div>
      </Form>
    </>
  );
};
