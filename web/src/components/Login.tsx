import { UserOutlined } from "@ant-design/icons";
import { Button, Form, Input, Space } from "antd";
import { useForm } from "antd/es/form/Form";

export const Login = ({ onSubmit }: { onSubmit: (email: string) => void }) => {
  const [form] = useForm();
  return (
    <Form
      form={form}
      onFinish={() => onSubmit(form.getFieldValue("email"))}
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
          onClick={() => {
            localStorage.setItem("email", form.getFieldValue("email"));
          }}
        >
          Log in
        </Button>
      </Form.Item>
    </Form>
  );
};
