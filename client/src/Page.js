export const Page = ({ page_num, setPage, isSelected }) => {
  return (
    <div
      onClick={() => setPage(page_num)}
      style={
        isSelected
          ? { padding: '5px', color: 'black' }
          : { padding: '5px', color: 'blue', textDecoration: 'underline', cursor: 'pointer' }
      }
    >
      {page_num}
    </div>
  );
};
