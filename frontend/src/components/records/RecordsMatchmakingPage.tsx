import React, { useEffect, useState } from 'react';
import { Table } from 'antd';
import axios from 'axios';

interface MatchmakingRecord {
  id: number;
  bride_name: string;
  bride_dob: string;
  bride_tob: string;
  bride_place: string;
  groom_name: string;
  groom_dob: string;
  groom_tob: string;
  groom_place: string;
  guna_score: number;
  compatibility: string;
  remarks: string;
  created_at: string;
}

const RecordsMatchmakingPage: React.FC = () => {
  const [data, setData] = useState<MatchmakingRecord[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    axios.get('/api/matchmaking/')
      .then(res => setData(res.data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h2>Matchmaking Records</h2>
      <Table
        dataSource={data}
        loading={loading}
        rowKey="id"
        columns={[
          { title: 'Bride Name', dataIndex: 'bride_name' },
          { title: 'Bride DOB', dataIndex: 'bride_dob' },
          { title: 'Bride TOB', dataIndex: 'bride_tob' },
          { title: 'Bride Place', dataIndex: 'bride_place' },
          { title: 'Groom Name', dataIndex: 'groom_name' },
          { title: 'Groom DOB', dataIndex: 'groom_dob' },
          { title: 'Groom TOB', dataIndex: 'groom_tob' },
          { title: 'Groom Place', dataIndex: 'groom_place' },
          { title: 'Guna Score', dataIndex: 'guna_score' },
          { title: 'Compatibility', dataIndex: 'compatibility' },
          { title: 'Remarks', dataIndex: 'remarks' },
          { title: 'Created At', dataIndex: 'created_at' },
        ]}
      />
    </div>
  );
};

export default RecordsMatchmakingPage; 