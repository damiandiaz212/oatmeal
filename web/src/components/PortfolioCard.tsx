import React, { useEffect, useRef, useState } from "react";
import { ArrowDownOutlined, ArrowUpOutlined } from "@ant-design/icons";
import { Card, Col, Row, Statistic, Spin, message } from "antd";
import { Typography } from "antd";
import { getPortfolioStatus } from "@/service/api";

const { Title } = Typography;

interface IOrder {
  order: string;
  symbol: string;
  amount: number;
}

const PortfolioCard = ({ id }: { id: string }) => {
  const [portfolio, setPortfolio] = useState<any>();
  const [data, setData] = useState<IOrder | null>(null);

  // useEffect(() => {
  //   const sse = new EventSource(`http://localhost:5000/api/stream?id=${id}`);
  //   sse.onmessage = (e) => setData(e.data);
  //   return () => {
  //     sse.close();
  //   };
  // }, []);

  // useEffect(() => {
  //   if (data) {
  //     console.log(data);
  //   }
  // }, [data]);

  useEffect(() => {
    async function fetchData() {
      const portfolio = await getPortfolioStatus(id);
      setPortfolio(portfolio);
    }
    fetchData();
  }, [id]);

  return (
    <>
      <div style={{ padding: "2rem", maxWidth: "250px" }}>
        <Spin spinning={!portfolio}>
          <Card
            title={portfolio?.name}
            bordered={false}
            style={{
              backgroundColor: "#5C5470",
            }}
          >
            <Row gutter={24}>
              <Col>
                <Statistic
                  title="Balance"
                  value={portfolio?.balance}
                  precision={2}
                  valueStyle={{ fontSize: "1rem", color: "white" }}
                  prefix="$"
                />
                <br />
                <Statistic
                  title="Gain / Loss"
                  value={portfolio && portfolio?.adj}
                  precision={2}
                  valueStyle={{
                    fontSize: "1rem",
                    color: "white",
                  }}
                  prefix="$"
                />
                <Statistic
                  value={0.0}
                  precision={2}
                  valueStyle={{
                    color: "#03C988",
                    fontSize: "1rem",
                    fontWeight: "700",
                  }}
                  prefix={<ArrowUpOutlined rev={undefined} />}
                  suffix="%"
                />
              </Col>
              <Col>
                <Statistic
                  title="Buying Power"
                  value={portfolio?.buying_power}
                  precision={2}
                  valueStyle={{ fontSize: "1rem", color: "white" }}
                  prefix="$"
                />
                <br />
              </Col>
            </Row>
          </Card>
        </Spin>
      </div>
    </>
  );
};

export default PortfolioCard;
