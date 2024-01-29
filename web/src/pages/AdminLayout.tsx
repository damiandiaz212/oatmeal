import { useEffect, useState } from "react";
import PortfolioCard from "../components/PortfolioCard";
import {
  deletePortfolio,
  getPortfolioIds,
  getPortfolioStatus,
} from "../service/api";
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

  const handleDelete = (id: string) => {
    deletePortfolio(id).then(() => {
      setIds(ids.filter((_id) => _id != id));
    });
  };

  return (
    <>
      <List
        grid={{
          gutter: 4,
        }}
        dataSource={ids}
        renderItem={(id) => (
          <List.Item>
            <PortfolioCard id={id} onDelete={(id) => handleDelete(id)} />
          </List.Item>
        )}
      />
    </>
  );
};

export default AdminLayout;
