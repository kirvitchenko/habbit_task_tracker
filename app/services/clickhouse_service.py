import clickhouse_connect

from app.core.config import CLICKHOUSE_PORT, CLICKHOUSE_HOST, CLICKHOUSE_USER, \
    CLICKHOUSE_PASSWORD


class ClickhouseDashboardService:
    _client = None

    async def get_client(self):
        if self._client is None:
            self._client = await clickhouse_connect.get_async_client(
                host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT, username=CLICKHOUSE_USER, password=CLICKHOUSE_PASSWORD
            )
        return self._client


class ClickhouseTaskDashBoardService(ClickhouseDashboardService):
    async def get_daily_stats(self):
        client = await self.get_client()
        query = """
            SELECT toDate(timestamp) as day, count() as total
            FROM task_events
            WHERE event_type = 'task.created'
            GROUP BY day
            ORDER BY day DESC
            LIMIT 30
        """
        result = await client.query(query)
        return [{"date": row[0], "count": row[1]} for row in result.result_rows]
