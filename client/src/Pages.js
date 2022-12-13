import { Page } from './Page';

export const Pages = ({ page, setPage, size, total }) => {
  const page_nums = [...Array(parseInt(total / size)).keys()].map((n) => ++n);
  return (
    <div
      style={{
        display: 'flex',
        flexFlow: 'row wrap',
        justifyContent: 'center',
      }}
    >
      {page_nums.map((page_num, id) => (
        <Page page_num={page_num} setPage={setPage} isSelected={page_num === page} key={id} />
      ))}
    </div>
  );
};
