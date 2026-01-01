import { useNavigate } from "react-router-dom";
import SigninInput from "../SigninInput";
import { useState } from "react";
import { useAuth } from "../../hooks/useAuth";
import axios from "../../api/axios";

export const Signup = () => {
  const navigation = useNavigate();
  const { signup, sevError, showAlert } = useAuth();

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    passwordConfirm: "",
  });

  const [error, setError] = useState({});
  const [usernameStatus, setUsernameStatus] = useState('idle'); // 'idle', 'checking', 'available', 'unavailable', 'error'

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
    if (name === "username") {
      setUsernameStatus('idle'); // Reset status when username changes
      setError(prev => ({ ...prev, name: "" })); // Clear username error
    }
  };

  const checkUsernameAvailability = async () => {
    if (!form.username.trim()) {
      setError(prev => ({ ...prev, name: "이름을 입력해주세요." }));
      setUsernameStatus('unavailable');
      return false;
    }
    if (form.username.trim().length < 3) {
      setError(prev => ({ ...prev, name: "이름은 3자 이상이어야 합니다." }));
      setUsernameStatus('unavailable');
      return false;
    }

    setUsernameStatus('checking');
    setError(prev => ({ ...prev, name: "" }));
    try {
      const response = await axios.post("/users/check-name", {
        username: form.username,
      });
      if (response.data.is_available) {
        setUsernameStatus('available');
        return true;
      } else {
        setUsernameStatus('unavailable');
        setError(prev => ({ ...prev, name: "이미 사용중인 이름입니다." }));
        return false;
      }
    } catch (error) {
      console.error("name check error", error);
      setUsernameStatus('error');
      setError(prev => ({ ...prev, name: "아이디 확인 중 오류 발생" }));
      return false;
    }
  };

  const validate = async () => {
    const newErrors = {};

    if (usernameStatus !== 'available') {
      newErrors.name = error.name || "아이디 중복 확인이 필요합니다.";
    }

    if (
      !/^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i.test(
        form.email
      )
    ) {
      newErrors.email = "올바른 이메일 형식이 아닙니다.";
    }

    if (!/^(?=.*[a-zA-Z])(?=.*[0-9]).{8,}$/.test(form.password)) {
      newErrors.password = "영문자와 숫자를 포함해 8자 이상이어야 합니다.";
    }

    if (form.password !== form.passwordConfirm) {
      newErrors.passwordConfirm = "비밀번호가 일치하지 않습니다";
    }

    setError(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handlesubmit = async (e) => {
    e.preventDefault();

    if (!(await validate())) return;

    if (usernameStatus !== 'available') {
      setError(prev => ({ ...prev, name: "아이디 중복 확인이 필요합니다." }));
      return;
    }

    const { email, username, password } = form;
    const success = await signup({ email, username, password });

    if (success) {
      // alert("회원가입이 완료되었습니다");
      showAlert("회원가입이 완료되었습니다.");

      navigation("/");
    } else {
      alert(sevError);
    }
  };

  const getUsernameInputClass = () => {
    let baseClass = "w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 shadow-gray-400";
    if (usernameStatus === 'available') return baseClass + " outline-main-green border border-main-green";
    if (usernameStatus === 'unavailable') return baseClass + " outline-red-500 border border-red-500";
    return baseClass + " outline-main-green"; // Default or idle state
  };

  const getUsernameFeedbackMessage = () => {
    if (usernameStatus === 'checking') return "(중복 확인 중...)";
    if (usernameStatus === 'available') return "(사용 가능한 아이디입니다.)";
    if (usernameStatus === 'unavailable') return "(이미 사용중인 아이디입니다.)";
    if (usernameStatus === 'error') return "(아이디 확인 중 오류 발생)";
    return "";
  };

  const getUsernameFeedbackColorClass = () => {
    if (usernameStatus === 'available') return "text-main-green";
    if (usernameStatus === 'unavailable') return "text-red-500";
    return "";
  };

  return (
    <>
      <div className="min-h-screen flex justify-center items-start pt-12">
        <div className="w-full max-w-md rounded-xl p-8">
          <div className="mb-10 text-custom-basic-font text-3xl">Signup</div>

          <form
            className="flex flex-col items-center w-full max-w-md mx-auto space-y-2"
            onSubmit={handlesubmit}
          >
            <div className="flex flex-col w-full px-2 sm:px-4">
              <div className="w-full">
                <SigninInput
                  title="name"
                  type="text"
                  name="username"
                  placeholder="이름을 입력해주세요"
                  value={form.username}
                  onChange={handleChange}
                  className={getUsernameInputClass()}
                />
                <div className="flex justify-end -mt-2 mb-2 pr-1">
                  <button
                    type="button"
                    className="px-4 py-1.5 text-xs font-bold border-2 rounded-full border-main-green bg-white text-main-green hover:bg-main-green hover:text-white transition-all active:scale-95 disabled:border-gray-300 disabled:text-gray-300 shadow-sm"
                    onClick={checkUsernameAvailability}
                    disabled={usernameStatus === 'checking' || !form.username.trim()}
                  >
                    중복 확인
                  </button>
                </div>
              </div>
              {(error.name || usernameStatus !== 'idle') && (
                <p className={`text-xs mt-0 text-right pr-2 mb-2 ${getUsernameFeedbackColorClass()}`}>
                  {error.name || getUsernameFeedbackMessage()}
                </p>
              )}
            </div>

            <div className="flex flex-col w-full px-2 sm:px-4">
              <SigninInput
                title="email"
                type="email"
                name="email"
                placeholder="이메일을 입력해주세요"
                value={form.email}
                onChange={handleChange}
              />
              {error.email && (
                <p className="text-red-500 text-xs mt-1 text-right pr-2">{error.email}</p>
              )}
            </div>

            <div className="flex flex-col w-full px-2 sm:px-4">
              <SigninInput
                title="pw"
                type="password"
                name="password"
                placeholder="비밀번호를 입력해주세요"
                value={form.password}
                onChange={handleChange}
              />
              {error.password && (
                <p className="text-red-500 text-xs mt-1 text-right pr-2">{error.password}</p>
              )}
            </div>

            <div className="flex flex-col w-full px-2 sm:px-4">
              <SigninInput
                title="pw confirm"
                type="password"
                name="passwordConfirm"
                placeholder="비밀번호를 다시 입력해주세요"
                value={form.passwordConfirm}
                onChange={handleChange}
              />
              {error.passwordConfirm && (
                <p className="text-red-500 text-xs mt-1 text-right pr-2">
                  {error.passwordConfirm}
                </p>
              )}
            </div>

            <div className="mt-8 flex justify-center w-full px-4 space-x-4">
              <button
                onClick={() => navigation("/")}
                type="button"
                className="bg-gray-200 text-gray-700 w-full sm:w-[120px] h-[45px] sm:h-[35px] rounded-lg font-medium active:scale-95 transition-transform"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="bg-main-green text-white w-full sm:w-[120px] h-[45px] sm:h-[35px] rounded-lg font-medium active:scale-95 transition-transform shadow-md"
              >
                Confirm
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};
