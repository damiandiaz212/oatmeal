import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Dropdown, MenuProps, Space, Spin } from "antd";
import { Login } from "@/components/Login";
import {
  DownOutlined,
  SettingOutlined,
  SmileOutlined,
} from "@ant-design/icons";

export const Serve = () => {
  const params = useParams();
  const [loading, setLoading] = useState(true);
  const [imgUrl, setImgUrl] = useState<any>();
  const [reqPayload, setReqPayload] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [email, setEmail] = useState("");

  useEffect(() => {
    const localEmail = localStorage.getItem("email");
    if (!localEmail) {
      setLoading(false);
    } else {
      setEmail(localEmail);
    }
  }, []);

  useEffect(() => {
    if (email) {
      setReqPayload({
        ref: params.ref,
        email: email,
      });
    }
  }, [email]);

  useEffect(() => {
    if (reqPayload && !imgUrl) {
      generateImage();
    }
  }, [reqPayload]);

  useEffect(() => {
    if (imgUrl) {
      setLoading(false);
    }
  }, [imgUrl]);

  const container = {
    textAlign: "center",
    overflow: "hidden",
  };

  const imgStyle = {
    height: "75%",
    width: "75%",
  };

  const buildText = {
    position: "absolute",
    bottom: "8px",
    right: "16px",
    fontWeight: "500",
    fontSize: "1rem",
    paddingBottom: "1rem",
  };

  const errorMessage = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    fontSize: "1rem",
    width: "500px",
  };

  const menuDropdown = {
    fontSize: "1.5rem",
    position: "absolute",
    marginLeft: "auto",
  };

  const errors = (err: string) => {
    switch (err) {
      case "EMAIL":
        return (
          <>
            <b>user not found</b>
            <p>
              You can create a new account{" "}
              <a href="/" target={"_blank"}>
                here
              </a>
            </p>
            <p>Then refresh page</p>
          </>
        );
      case "GENERIC":
        return (
          <>
            <b>Generic server error</b>
            <p>Refresh page to try again</p>
          </>
        );
    }
  };

  const items: MenuProps["items"] = [
    {
      key: "1",
      label: (
        <a
          target="_blank"
          rel="noopener noreferrer"
          onClick={() => {
            generateImage();
          }}
        >
          Refresh
        </a>
      ),
    },
    {
      key: "2",
      label: (
        <a
          target="_blank"
          rel="noopener noreferrer"
          onClick={() => {
            setEmail("");
            localStorage.removeItem("email");
          }}
        >
          Log out
        </a>
      ),
      danger: true,
    },
  ];

  async function generateImage() {
    const queryString = new URLSearchParams(window.location.search);
    const urlParams = new URLSearchParams(queryString);
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      mode: "cors",
      body: JSON.stringify({
        email: reqPayload.email,
      }),
    };
    setLoading(true);
    return fetch(
      `http://localhost:5000/api/generate?ref=${reqPayload.ref}`,
      requestOptions
    )
      .then((response) => {
        if (response.status == 404) {
          setLoading(false);
          setError("EMAIL");
        } else if (response.status == 500) {
          setLoading(false);
          setError("GENERIC");
        }
        return response.json();
      })
      .then((json) => setImgUrl(json.img));
  }

  return (
    <div style={container}>
      {email ? (
        <>
          {!loading && !error && (
            <div style={menuDropdown}>
              <Dropdown menu={{ items }}>
                <a onClick={(e) => e.preventDefault()}>
                  <Space>
                    <SettingOutlined rev={undefined} />
                  </Space>
                </a>
              </Dropdown>
            </div>
          )}
          <div style={buildText}>{!loading && !error && "ALPHA BUILD"}</div>
          {!loading && !error ? (
            <img src={imgUrl} style={imgStyle} />
          ) : (
            <Spin />
          )}
          <div style={errorMessage}>
            <>
              {error && !loading && `There was a problem: `}
              {error && !loading && errors(error)}
            </>
          </div>
        </>
      ) : (
        <Login onSubmit={(value) => setEmail(value)} />
      )}
    </div>
  );
};
