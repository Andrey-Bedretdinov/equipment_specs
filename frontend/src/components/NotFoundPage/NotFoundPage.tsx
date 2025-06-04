import { Result, Button } from 'antd'
import { Link } from 'react-router-dom'

const NotFoundPage = () => (
  <Result
    status="404"
    title="404"
    subTitle="Извините, страница не найдена."
    extra={
      <Link to="/">
        <Button type="primary">Вернуться на главную</Button>
      </Link>
    }
  />
)

export default NotFoundPage;