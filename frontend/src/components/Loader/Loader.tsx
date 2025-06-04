import { Button, Result, Spin } from "antd";

interface LoaderProps {
    isLoading: boolean;
    isError: boolean;
}

const Loader: React.FC<LoaderProps> = ({ isLoading, isError }) => {
    return (
        <>
            {isLoading && (
                <div style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    minHeight: '50vh',
                }}>
                    <Spin size="large" />
                </div>
            )}

            {
                isError && (
                    <Result
                        status="error"
                        title="Произошла ошибка"
                        subTitle="Не удалось загрузить список проектов. Попробуйте позже."
                        extra={[
                            <Button
                                key='reload'
                                type="primary"
                                onClick={() => window.location.reload()}
                            >
                                Обновить
                            </Button>,
                        ]}
                    />
                )
            }
        </>
    )
}

export default Loader;