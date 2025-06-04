import React from 'react';
import styles from './NavBar.module.css';
import { Typography, Dropdown } from 'antd';
import type { MenuProps } from 'antd';
import { useNavigate } from 'react-router-dom';

const { Title } = Typography;

const Navbar: React.FC = () => {
  const navigate = useNavigate();

  const catalogItems: MenuProps['items'] = [
    {
      key: 'kts',
      label: <span onClick={() => navigate('/catalog/kts')}>КТС</span>,
    },
    {
      key: 'units',
      label: <span onClick={() => navigate('/catalog/units')}>UNITS</span>,
    },
    {
      key: 'items',
      label: <span onClick={() => navigate('/catalog/items')}>ITEMS</span>,
    },
  ];

  return (
    <div className={styles.header}>
      <div className={styles.headerBox}>
        <Title level={3} style={{ color: 'black', margin: 0 }}>
          MyApp
        </Title>
        <div className={styles.headerItems}>
          <div className={styles.headerItem} onClick={() => navigate('/')}>
            Проекты
          </div>
          <Dropdown menu={{ items: catalogItems }} trigger={['hover']}>
            <div className={styles.headerItem}>
              Каталог
            </div>
          </Dropdown>
        </div>
      </div>
    </div>
  );
};

export default Navbar;
