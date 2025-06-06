import { Button, Typography } from "antd";
import { PlusOutlined } from '@ant-design/icons';
import { useGetCatalogItemsQuery } from "../../redux/services/catalogApi";
import Loader from "../../components/Loader/Loader";
import ItemCardsList from "../../components/ItemCardsList/ItemCardsList";
import { useState } from "react";
import AddItemModal from "../../components/AddItemModal/AddItemModal";

const { Title } = Typography;

const CatalogItemPage: React.FC = () => {

    const { data: items_list, isLoading, isError } = useGetCatalogItemsQuery();
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

    return (
        <>
            <div style={{ display: 'flex', gap: 16, alignItems: 'flex-end', marginBottom: 16 }}>
                <Title style={{ margin: 0 }}>Каталог Items</Title>
                <Button
                    type="primary"
                    icon={<PlusOutlined />}
                    onClick={() => setIsModalOpen(true)}
                />
            </div>


            {(isLoading || isError) ? (
                <Loader isLoading={isLoading} isError={isError} />
            ) : (
                <ItemCardsList items_list={items_list ?? []} />
            )}

            <AddItemModal 
                isModalOpen={isModalOpen}
                onCancel={() => setIsModalOpen(false)} 
            />
        </>
    );
}

export default CatalogItemPage;