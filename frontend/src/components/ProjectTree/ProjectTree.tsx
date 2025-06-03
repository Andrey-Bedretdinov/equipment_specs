import React from 'react';
import { Card, Typography, Space, Button } from 'antd';
import type { ProjectNode } from '../../types/types';
import KtcBlock from '../KtsBlock/KtsBlock';
import styles from './ProjectTree.module.css';

const { Title, Text } = Typography;

interface ProjectTreeProps {
    data: ProjectNode[];
}

const ProjectTree: React.FC<ProjectTreeProps> = ({ data }) => {
    return (
        <Space direction="vertical" className={styles.wrapper}>
            {data.map((project) => (
                <Card
                    key={project.id}
                    title={<Title level={3}>{project.name}</Title>}
                    className={styles.projectCard}
                >
                    <Text>{project.description}</Text>
                    <div className={styles.projectDescription}>
                        <div className={styles.sectionHeader}>
                            <Title level={4}>КТС:</Title>
                            <Button>Добавить</Button>
                        </div>

                        <Space direction="vertical" style={{ width: '100%' }}>
                            {project.kts.map((ktc) => <KtcBlock key={ktc.id} ktc={ktc} />)}
                        </Space>
                    </div>
                </Card>
            ))}
        </Space>
    );
};

export default ProjectTree;
