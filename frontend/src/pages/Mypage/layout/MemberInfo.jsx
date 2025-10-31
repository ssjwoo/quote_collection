import { useEffect, useState } from "react";
import { Form } from "react-router-dom";
import axios from "../../../api/axios";

export const MemberInfo = () => {
  const [user, setUser] = useState(null);
  const [name, setName] = useState("");
  const [pw, setPw] = useState("");
  const [confirmedPw, setConfirmedPw] = useState("");
  const [error, setError] = useState({ nameE: "", pwE: "", confirmedPwE: "" });
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem("accessToken");
        if (token) {
          // TODO: /api/auth/me
          const response = await axios.get("/auth/me", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          console.log("/api/auth/me", response);
          const userData = response.data;
          setUser(userData);
          setName(userData.username);
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
    if (user && user.username === name.trim()) setChecked(true);
    else setChecked(false);
  }, [name, user]);

  const onIdCheck = async () => {
    try {
      // TODO: /api/users/check-name
      const response = await axios.post("/users/check-name", {
        username: name,
      });
      console.log("/api/users/check-name", response);
      const data = response.data;
      setChecked(data.is_available);
      if (!data.is_available) {
        alert("이미 사용중인 아이디입니다.");
      }
    } catch (error) {
      console.error("Failed to check name:", error);
    }
  };

  const onsubmit = async (e) => {
    e.preventDefault();

    if (user.username === name.trim() && !pw && !confirmedPw) {
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

      // TODO: /api/users/${user.id}, no navigation
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
               className="p-0.5 pl-1 pr-1 text-xs border rounded-sm border-main-green hover:ring-1 hover:ring-main-green
             disabled:border-gray-400 disabled:text-gray-400 disabled:hover:ring-0 "
              onClick={onIdCheck}
              disabled={user && user.username === name.trim()}
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
