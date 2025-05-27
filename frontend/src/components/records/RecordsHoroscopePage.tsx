import React, { useEffect, useState } from 'react';
import { Table, Image, Button, Modal } from 'antd';
import axios from 'axios';
import { EyeOutlined } from '@ant-design/icons';

interface HoroscopeRecord {
  id: number;
  name: string;
  date_of_birth: string;
  time_of_birth: string;
  place_name: string;
  rashi: string;
  nakshatra: string;
  lagna: string;
  created_at: string;
  chart_image?: string;
  planetary_positions?: any;
}

const RecordsHoroscopePage: React.FC = () => {
  const [data, setData] = useState<HoroscopeRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [viewRecord, setViewRecord] = useState<HoroscopeRecord | null>(null);

  useEffect(() => {
    setLoading(true);
    axios.get('/api/horoscope/')
      .then(res => setData(res.data))
      .finally(() => setLoading(false));
  }, []);

  const renderPlanetaryTable = (positions: any) => (
    <Table
      dataSource={Object.entries(positions).map(([planet, details]) => {
        // Ensure details is an object
        if (typeof details === 'object' && details !== null) {
          return { planet, ...details };
        } else {
          return { planet };
        }
      })}
      columns={[
        { title: 'Planet', dataIndex: 'planet' },
        { title: 'Positions', dataIndex: 'dms' },
        { title: 'Degree', dataIndex: 'dms_in_sign' },
        { title: 'Rasi', dataIndex: 'rasi' },
        { title: 'Rasi Lord', dataIndex: 'rasi_lord' },
        { title: 'Nakshatra', dataIndex: 'nakshatra' },
        { title: 'Nakshatra Lord', dataIndex: 'nakshatra_lord' },
        { title: 'Retrograde', dataIndex: 'retrograde', render: (v: boolean) => v ? '℞' : '' },
      ]}
      pagination={false}
      rowKey="planet"
      size="small"
    />
  );

  return (
    <div>
      <h2>Horoscope Records</h2>
      <Table
        dataSource={data}
        loading={loading}
        rowKey="id"
        columns={[
          { title: 'Name', dataIndex: 'name' },
          { title: 'DOB', dataIndex: 'date_of_birth' },
          { title: 'TOB', dataIndex: 'time_of_birth' },
          { title: 'Place', dataIndex: 'place_name' },
          { title: 'Rashi', dataIndex: 'rashi' },
          { title: 'Nakshatra', dataIndex: 'nakshatra' },
          { title: 'Lagna', dataIndex: 'lagna' },
          { title: 'Created At', dataIndex: 'created_at' },
          {
            title: 'Chart Image',
            dataIndex: 'chart_image',
            render: (value: string | undefined) => {
              console.log('Chart image value:', value);
              if (!value) return null;
              const parts = value.split('/horoscope_charts/');
              const filename = parts.length > 1 ? parts[1] : '';
              const url = filename ? `/static/horoscope_charts/${filename}` : '';
              return url ? (
                <Image width={60} src={url} alt="Chart" />
              ) : null;
            }
          },
          {
            title: 'Actions',
            render: (_, record) => (
              <EyeOutlined
                style={{ fontSize: 20, cursor: 'pointer', color: '#1890ff' }}
                onClick={() => setViewRecord(record)}
                title="View planetary positions"
              />
            )
          }
        ]}
      />

      <Modal
        open={!!viewRecord}
        onCancel={() => setViewRecord(null)}
        title={viewRecord ? `Planetary Positions for ${viewRecord.name}` : ''}
        footer={null}
        width={800}
      >
        {viewRecord && viewRecord.planetary_positions && renderPlanetaryTable(viewRecord.planetary_positions)}
      </Modal>
    </div>
  );
};

export default RecordsHoroscopePage; 