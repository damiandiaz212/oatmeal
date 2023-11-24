import "./Land.scss";
import {
  Layout,
  theme,
  Button,
  Flex,
  Form,
  message,
  Input,
  Result,
} from "antd";
import logo from "./images/landBW.png";
import { AppleFilled, GoogleOutlined } from "@ant-design/icons";
import { InteractiveImage } from "@/components/InteractiveImage";
import { CreateAccount } from "../account/CreateAccount";
import { useState } from "react";
const { Content, Footer, Header } = Layout;

export function Land() {
  const {
    token: { colorBgContainer, colorText, colorPrimary },
  } = theme.useToken();
  const [form] = Form.useForm();

  const onFinish = () => {
    message.success("Submit success!");
  };

  const onFinishFailed = () => {
    message.error("Submit failed!");
  };

  const onFill = () => {
    form.setFieldsValue({
      url: "https://taobao.com/",
    });
  };

  function handleRegister(email: string) {
    console.log(`User registered!: ${email}`);
    setSuccess(true);
  }

  const [accountFormOpen, setAccountFormOpen] = useState(false);
  const [success, setSuccess] = useState(false);

  return (
    <>
      <CreateAccount
        open={accountFormOpen}
        onComplete={() => {
          handleRegister("damiandiaz2025@gmail.com");
          setAccountFormOpen(false);
        }}
      />
      <Layout
        style={{ height: "100%", width: "60vw", background: colorBgContainer }}
      >
        <Content
          style={{
            height: "100%",
            width: "100%",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div
            style={{
              marginLeft: "-50rem",
              marginTop: "-15rem",
              opacity: "0.5",
            }}
          >
            <InteractiveImage src={logo} width={350} alt="" />
          </div>
          <div
            className="scrolling-words-container"
            style={{
              paddingLeft: "0.5rem",
              position: "absolute",
            }}
          >
            <span
              style={{
                color: "white",
                backgroundColor: colorPrimary,
                padding: "0.5rem",
                borderRadius: "5px",
                width: "100px",
                textAlign: "center",
                border: "4px solid white",
              }}
            >
              <div className="divSquare">W</div>
              <div className="divSquare">E</div>
              <div style={{ clear: "both" }} />
              <div className="divSquare">A</div>
              <div className="divSquare">R</div>
            </span>
            <div className="scrolling-words-box">
              <ul>
                <li style={{ color: colorPrimary }}>Anything</li>
                <li style={{ color: colorPrimary }}>Virtually</li>
                <li style={{ color: colorPrimary }}>Confidently</li>
              </ul>
            </div>
          </div>
        </Content>
        <Content
          style={{
            height: "100%",
            width: "100%",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            paddingTop: "8rem",
          }}
        >
          <Flex vertical gap="small" style={{ width: "25%" }}>
            {!success ? (
              <>
                <Form
                  form={form}
                  onFinish={onFinish}
                  onFinishFailed={onFinishFailed}
                  autoComplete="off"
                >
                  <Form.Item name="email">
                    <Input placeholder="Email address" size="large" />
                  </Form.Item>
                  <Form.Item>
                    <Button
                      type="primary"
                      htmlType="submit"
                      style={{ width: "100%" }}
                    >
                      Log in
                    </Button>
                    Dont have an account?{" "}
                    <a onClick={() => setAccountFormOpen(true)}>Sign up</a>
                  </Form.Item>
                </Form>
                <Button disabled>
                  Continue with Google <GoogleOutlined rev="" />
                </Button>
                <Button disabled>
                  Continue with Apple <AppleFilled rev="" />
                </Button>
              </>
            ) : (
              <Result
                status="success"
                title="Successfully Registered"
                subTitle="You're now able to use oatmeal on any of our supported platforms!"
                style={{ width: "300px", textAlign: "center" }}
              />
            )}
          </Flex>
        </Content>
      </Layout>
    </>
  );
}
