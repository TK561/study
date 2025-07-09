function convertToJST(utcTimeString) {
    try {
        const today = new Date();
        const [time, ampm] = utcTimeString.split(' ');
        const [hours, minutes, seconds] = time.split(':').map(Number);
        
        let hour24 = hours;
        if (ampm === 'PM' && hours !== 12) {
            hour24 += 12;
        } else if (ampm === 'AM' && hours === 12) {
            hour24 = 0;
        }
        
        const utcDate = new Date(today.getFullYear(), today.getMonth(), today.getDate(), hour24, minutes, seconds);
        const jstDate = new Date(utcDate.getTime() + (9 * 60 * 60 * 1000));
        
        const jstHour = jstDate.getHours();
        const jstMinute = jstDate.getMinutes();
        const jstSecond = jstDate.getSeconds();
        
        const jstHour12 = jstHour === 0 ? 12 : jstHour > 12 ? jstHour - 12 : jstHour;
        const jstAmPm = jstHour < 12 ? 'AM' : 'PM';
        
        return `${jstHour12.toString().padStart(2, '0')}:${jstMinute.toString().padStart(2, '0')}:${jstSecond.toString().padStart(2, '0')} ${jstAmPm}`;
    } catch (error) {
        return utcTimeString;
    }
}

console.log('UTC 01:00:00 AM -> JST:', convertToJST('01:00:00 AM'));
console.log('UTC 06:00:00 AM -> JST:', convertToJST('06:00:00 AM'));
console.log('Current time:', new Date().toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' }));