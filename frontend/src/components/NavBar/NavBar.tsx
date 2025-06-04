import React from 'react';
import styles from './NavBar.module.css'
import { Typography } from 'antd';
import { useNavigate } from 'react-router-dom';
const { Title } = Typography;

const Navbar: React.FC = () => {

  const navigate = useNavigate();

  return (
    <div
      className={styles.header}
    >
      <div className={styles.headerBox}>
        <Title level={3} style={{ color: 'Black', margin: 0 }}>
          MyApp
        </Title>
        <div className={styles.headerItems}>
          <div
            className={styles.headerItem}
            onClick={() => navigate('/')}
          >
            Проекты</div>
          <div
            className={styles.headerItem}
            onClick={() => navigate('/catalog')}
          >
            Каталог</div>
        </div>
      </div>
    </div>
  );
};

export default Navbar;
