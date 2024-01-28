import { useEffect, useState } from "react";
import PortfolioCard from "../components/PortfolioCard";
import { getPortfolioIds, getPortfolioStatus } from "../service/api";
import { List } from "antd";

const AdminLayout = () => {
  const [ids, setIds] = useState<string[]>([]);

  useEffect(() => {
    async function fetchData() {
      const ids = await getPortfolioIds();
      setIds(ids);
    }
    fetchData();
  }, []);

  return (
    <>
      <List
        grid={{
          gutter: 4,
        }}
        dataSource={ids}
        renderItem={(id) => (
          <List.Item>
            <PortfolioCard id={id} />
          </List.Item>
        )}
      />
    </>
  );
};

export default AdminLayout;
