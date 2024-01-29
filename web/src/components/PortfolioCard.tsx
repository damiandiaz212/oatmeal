import React, { useEffect, useRef, useState } from "react";
import {
  ArrowDownOutlined,
  ArrowUpOutlined,
  CopyOutlined,
  DeleteColumnOutlined,
  DeleteFilled,
  DeleteOutlined,
  SettingFilled,
  SettingOutlined,
} from "@ant-design/icons";
import {
  Card,
  Col,
  Row,
  Statistic,
  Spin,
  message,
  List,
  Badge,
  Button,
  Space,
  Dropdown,
} from "antd";
import { Typography } from "antd";
import { getPortfolioStatus, getTransactions } from "@/service/api";

const { Title } = Typography;

interface IOrder {
  order: string;
  symbol: string;
  amount: number;
}

const PortfolioCard = ({
  id,
  onDelete,
}: {
  id: string;
  onDelete: (id: string) => void;
}) => {
  const [portfolio, setPortfolio] = useState<any>();
  const [data, setData] = useState<IOrder | null>(null);
  const [transactions, setTransactions] = useState();

  useEffect(() => {
    async function fetchData() {
      const portfolio = await getPortfolioStatus(id);
      const transactions = await getTransactions(id);
      setPortfolio(portfolio);
      setTransactions(transactions.reverse());
    }
    fetchData();
  }, [id]);

  const getOrderEntry = (item: any) => {
    return (
      <>
        <div
          style={{
            backgroundColor: item[1] === "sell" ? "#346751" : "#C84B31",
            padding: "0.1rem 0.3rem 0.1rem 0.3rem",
            borderRadius: "3px",
            fontWeight: "700",
          }}
        >
          {item[1].toUpperCase()}
        </div>
        &nbsp;{item[2].toUpperCase()} x {item[3]} @ ${item[4]}
      </>
    );
  };

  const calculateAdj = () => {
    if (portfolio) {
      return (
        ((portfolio.balance - portfolio.starting) / portfolio.starting) * 100
      );
    } else {
      return 0.0;
    }
  };

  const items = [
    {
      key: "1",
      label: (
        <a
          target="_blank"
          rel="noopener noreferrer"
          onClick={() => navigator.clipboard.writeText(portfolio.id)}
        >
          Copy ID <CopyOutlined style={{ color: "grey" }} rev={undefined} />
        </a>
      ),
    },
    {
      key: "2",
      danger: true,
      label: (
        <a
          target="_blank"
          rel="noopener noreferrer"
          onClick={() => onDelete(portfolio.id)}
        >
          Delete
        </a>
      ),
    },
  ];

  return (
    <>
      <div style={{ padding: "2rem" }}>
        <Spin spinning={!portfolio}>
          <Card
            title={portfolio?.name}
            bordered={false}
            extra={
              <Dropdown menu={{ items }}>
                <a onClick={(e) => e.preventDefault()}>
                  <Space>
                    <SettingOutlined
                      style={{ color: "grey" }}
                      rev={undefined}
                    />
                  </Space>
                </a>
              </Dropdown>
            }
          >
            <Row gutter={24}>
              <Col>
                <Statistic
                  title="Balance"
                  value={portfolio?.balance}
                  precision={2}
                  valueStyle={{ fontSize: "1rem" }}
                  prefix="$"
                />
                <br />
                <Statistic
                  title="Gain / Loss"
                  value={portfolio && portfolio?.adj}
                  precision={2}
                  valueStyle={{
                    fontSize: "1rem",
                  }}
                  prefix="$"
                />
                <br />
                <Statistic
                  title="Buying Power"
                  value={portfolio?.buying_power}
                  precision={2}
                  valueStyle={{ fontSize: "1rem" }}
                  prefix="$"
                />
              </Col>
              <Col>
                <div
                  id="scrollableDiv"
                  style={{
                    height: 225,
                    overflow: "auto",
                    width: 200,
                    padding: "1rem",
                  }}
                >
                  <List
                    dataSource={transactions}
                    renderItem={(item: any) => (
                      <List.Item>{getOrderEntry(item)}</List.Item>
                    )}
                  />
                </div>
              </Col>
            </Row>
            <br />
            <Row>
              <Col>
                <Statistic
                  value={calculateAdj()}
                  precision={2}
                  valueStyle={{
                    fontSize: "2rem",
                    fontWeight: "600",
                    color: calculateAdj() >= 0 ? "#346751" : "#C84B31",
                  }}
                  prefix={
                    calculateAdj() > 0 ? (
                      <ArrowUpOutlined rev={undefined} />
                    ) : (
                      <ArrowDownOutlined rev={undefined} />
                    )
                  }
                  suffix="%"
                />
              </Col>
            </Row>
          </Card>
        </Spin>
      </div>
    </>
  );
};

export default PortfolioCard;
