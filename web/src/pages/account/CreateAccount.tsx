// @ts-nocheck
import { useEffect, useState } from "react";
import { Checkbox, Form, Input, Modal, Upload, Button } from "antd";
import type { UploadFile } from "antd/es/upload/interface";
import { UploadOutlined } from "@ant-design/icons";

export const CreateAccount = ({
  open,
  onComplete,
}: {
  open: boolean;
  onComplete: () => void;
}) => {
  const [form] = Form.useForm();
  const [accountInfo, setAccountInfoSubmitted] = useState(false);
  const [imageUploaded, setImageUploaded] = useState(false);
  const [email, setEmail] = useState("");
  const handleProgress = () => {
    if (accountInfo && !imageUploaded) {
      setAccountInfoSubmitted(false);
      onComplete();
    } else {
      setAccountInfoSubmitted(true);
    }
  };
  const handleCancel = () => {
    setAccountInfoSubmitted(false);
    setImageUploaded(false);
    onComplete();
  };
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const [uploading, setUploading] = useState(false);
  const formItemLayout = {
    labelCol: {
      xs: { span: 24 },
      sm: { span: 8 },
    },
    wrapperCol: {
      xs: { span: 24 },
      sm: { span: 16 },
    },
  };
  const tailFormItemLayout = {
    wrapperCol: {
      xs: {
        span: 24,
        offset: 0,
      },
      sm: {
        span: 16,
        offset: 8,
      },
    },
  };
  const props: UploadProps = {
    onRemove: (file) => {
      const index = fileList.indexOf(file);
      const newFileList = fileList.slice();
      newFileList.splice(index, 1);
      setFileList(newFileList);
    },
    beforeUpload: (file) => {
      setFileList([...fileList, file]);
      return false;
    },
    fileList,
  };
  return (
    <>
      <Modal
        title="Create an account"
        open={open}
        onOk={() => handleProgress()}
        onCancel={() => handleCancel()}
        okText={!accountInfo ? "Next" : "Submit"}
      >
        {!accountInfo && (
          <Form
            {...formItemLayout}
            form={form}
            name="register"
            style={{ maxWidth: 600 }}
            scrollToFirstError
          >
            <Form.Item
              name="email"
              label="E-mail"
              rules={[
                {
                  type: "email",
                  message: "The input is not valid E-mail!",
                },
                {
                  required: true,
                  message: "Please input your E-mail!",
                },
              ]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              name="agreement"
              valuePropName="checked"
              rules={[
                {
                  validator: (_, value) =>
                    value
                      ? Promise.resolve()
                      : Promise.reject(new Error("Should accept agreement")),
                },
              ]}
              {...tailFormItemLayout}
            >
              <Checkbox>
                I have read the <a href="/hello">agreement</a>
              </Checkbox>
            </Form.Item>
          </Form>
        )}
        {accountInfo && !imageUploaded && (
          <Form
            {...formItemLayout}
            form={form}
            name="register"
            style={{ maxWidth: 600 }}
            scrollToFirstError
          >
            <Form.Item
              name="image"
              label="Upload profile image"
              rules={[{ required: true }]}
            >
              <Upload
                action={`http://localhost:5000/api/create/${form.getFieldValue(
                  "email"
                )}`}
                listType="picture"
                maxCount={1}
              >
                <Button icon={<UploadOutlined rev="" />}>Upload</Button>
              </Upload>
            </Form.Item>
          </Form>
        )}
      </Modal>
    </>
  );
};
