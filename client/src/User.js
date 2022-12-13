export const User = ({ name, email, picture_url }) => {
  return (
    <div
      style={{
        border: '1px solid black',
        borderRadius: '5px',
        backgroundColor: '#fffbd4',
        margin: '10px',
        padding: '10px',
        maxHeight: '350px',
        maxWidth: '300px',
      }}
    >
      <div style={{ width: '70%', margin: 'auto' }}>
        <img src={picture_url} alt='' style={{ width: '100%' }} />
      </div>
      <h4>Name: {name}</h4>
      <h4>email: {email}</h4>
    </div>
  );
};
